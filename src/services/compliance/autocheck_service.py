import hashlib
import ipaddress
import json
import logging
import time
from dataclasses import asdict
from datetime import date, datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any

import redis
from sqlalchemy.orm import Session

from src.core.api_key import hash_api_key
from src.core.alerting import maybe_alert
from src.core.request_id import get_request_id
from src.domain.decisions import (
    DecisionStatus,
    Requirement,
    RequirementCategory,
    RequirementStatus,
    RuleExecutionRecord,
)
from src.domain.journey import Journey, JourneySegment, TransitPoint
from src.domain.passenger import ExistingVisa, Passenger, PassportInfo
from src.enums.decision import Decision
from src.enums.http_method import HTTPMethod
from src.exceptions.base import AppException
from src.exceptions.compliance.autocheck import (
    ClientExpiredError,
    ClientInactiveError,
    InvalidAPIKeyError,
    IPNotWhitelistedError,
    NoApplicableRulesError,
    RateLimitExceededError,
    UnknownReferenceDataError,
)
from src.models.administration.api_client import APIClient
from src.models.compliance.compliance_check import ComplianceCheck
from src.models.rule_management.rule_version import RuleVersion
from src.repositories.administration.api_client import APIClientRepository
from src.rule_engine.engine import RuleEngine
from src.rule_engine.models import JourneyRequest, RuleEngineResult
from src.schemas.administration.api_request_log import (
    APIRequestLogCreate,
)
from src.schemas.compliance.autocheck import (
    AutoCheckRequest,
    AutoCheckResponse,
    ComplianceDecisionResponse,
    CustomsRequirementResponse,
    EntryRestrictionResponse,
    HealthRequirementResponse,
    ImmigrationRequirementResponse,
    PassportRequirementResponse,
    TransitRequirementResponse,
    VisaRequirementResponse,
)
from src.schemas.compliance.compliance_check import ComplianceCheckCreate
from src.schemas.compliance.rule_execution_log import RuleExecutionLogCreate
from src.services.administration.api_request_log import (
    APIRequestLogService,
)
from src.services.administration.client_ip_whitelist import (
    ClientIPWhitelistService,
)
from src.services.compliance.compliance_check import ComplianceCheckService
from src.services.compliance.rule_execution_log import (
    RuleExecutionLogService,
)

logger = logging.getLogger(__name__)


_STATUS_TO_DECISION = {
    # DecisionStatus (5 values) -> the DB's Decision enum (3 values).
    # UNKNOWN deliberately maps to CONDITIONAL, never ALLOWED --
    # missing regulatory data must never present as "you're clear."
    DecisionStatus.CLEAR: Decision.ALLOWED,
    DecisionStatus.ACTION_REQUIRED: Decision.CONDITIONAL,
    DecisionStatus.CONDITIONAL: Decision.CONDITIONAL,
    DecisionStatus.NOT_PERMITTED: Decision.NOT_ALLOWED,
    DecisionStatus.UNKNOWN: Decision.CONDITIONAL,
}


def _json_safe(value: Any) -> Any:
    """Make dataclass output (Decimal, date, Enum) safe for a JSONB column."""

    def default(obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    return json.loads(json.dumps(value, default=default))


class AutoCheckService:
   

    def __init__(
        self,
        api_client_repository: APIClientRepository,
        client_ip_whitelist_service: ClientIPWhitelistService,
        api_request_log_service: APIRequestLogService,
        compliance_check_service: ComplianceCheckService,
        rule_execution_log_service: RuleExecutionLogService,
        redis_client: redis.Redis,
    ) -> None:
        self.api_client_repository = api_client_repository
        self.client_ip_whitelist_service = client_ip_whitelist_service
        self.api_request_log_service = api_request_log_service
        self.compliance_check_service = compliance_check_service
        self.rule_execution_log_service = rule_execution_log_service
        self.redis_client = redis_client

    # ------------------------------------------------------------------
    # Pipeline stages 1-4: everything the Rule Engine must never see if
    # the caller isn't a valid, active, whitelisted, within-limit client.
    # ------------------------------------------------------------------

    def _validate_api_key(self, db: Session, api_key: str, client_ip: str) -> APIClient:
        """1. API Key Validation.

        Looks up the hashed (SHA-256) portal-issued key first -- this
        is the path every client created through the self-service
        portal uses. Falls back to the legacy plaintext `api_key`
        column only so clients seeded before the portal existed (e.g.
        the demo client) keep working without needing to re-register.
        """

        client = self.api_client_repository.get_by_api_key_hash(
            db,
            hash_api_key(api_key),
        )

        if client is None:
            client = self.api_client_repository.get_by_api_key(db, api_key)

        if client is None:
            maybe_alert("invalid_api_key", client_ip)
            raise InvalidAPIKeyError()

        return client

    def _check_client_status(self, client: APIClient) -> None:
        """2. Client Status Check."""

        if not client.status:
            raise ClientInactiveError()

        if client.expires_at is not None:
            expires_at = client.expires_at

            # The DB column is a plain (non-tz) TIMESTAMP, so values read
            # back from Postgres are always naive -- but an in-memory
            # object set with an aware datetime before being persisted
            # could still carry tzinfo. Normalize both cases to naive UTC
            # before comparing, rather than branching on whichever one
            # happens to show up (that branch previously compared aware
            # vs. naive inconsistently depending on how the row was
            # populated).
            if expires_at.tzinfo is not None:
                expires_at = expires_at.astimezone(timezone.utc).replace(
                    tzinfo=None
                )

            now = datetime.now(timezone.utc).replace(tzinfo=None)

            if expires_at < now:
                raise ClientExpiredError(expires_at.isoformat())

    def _check_ip_whitelist(
        self,
        db: Session,
        client: APIClient,
        client_ip: str,
    ) -> None:
        """3. IP Whitelist Check.

        A client with no active whitelist entries at all is treated as
        unrestricted (no whitelist configured). Once at least one active
        entry exists, the caller's IP must match one of them, either
        exactly or within a CIDR range.
        """

        entries = self.client_ip_whitelist_service.get_client_whitelist_entries(
            db,
            client.id,
        )
        active_entries = [entry for entry in entries if entry.active]

        if not active_entries:
            return

        try:
            ip_obj = ipaddress.ip_address(client_ip)
        except ValueError:
            logger.warning(
                f"IP whitelist rejected client '{client.client_code}': "
                f"'{client_ip}' is not a parseable IP"
            )
            maybe_alert("ip_whitelist_rejected", client_ip, {"client_code": client.client_code})
            raise IPNotWhitelistedError(client_ip) from None

        for entry in active_entries:
            if entry.ip_address and entry.ip_address == client_ip:
                return

            if entry.cidr_range:
                try:
                    network = ipaddress.ip_network(entry.cidr_range, strict=False)
                except ValueError:
                    continue

                if ip_obj in network:
                    return

        logger.warning(
            f"IP whitelist rejected client '{client.client_code}': "
            f"'{client_ip}' matches no active entry"
        )
        maybe_alert("ip_whitelist_rejected", client_ip, {"client_code": client.client_code})
        raise IPNotWhitelistedError(client_ip)

    def _check_rate_limit(self, client: APIClient) -> None:
        """4. Rate Limiting (Redis).

        Fixed one-minute window per client, enforced via a Redis
        counter (INCR + EXPIRE). If Redis itself is unreachable, the
        check fails open (logged, request allowed) rather than taking
        the API down over an unavailable cache.
        """

        window = int(time.time() // 60)
        key = f"ratelimit:autocheck:{client.id}:{window}"

        try:
            current = self.redis_client.incr(key)
            if current == 1:
                self.redis_client.expire(key, 60)
        except redis.exceptions.RedisError as exc:
            logger.warning("Rate limiting unavailable (%s); allowing request.", exc)
            return

        if current > client.requests_per_minute:
            logger.warning(
                f"Rate limit exceeded for client '{client.client_code}' "
                f"({current}/{client.requests_per_minute} per minute)"
            )
            maybe_alert("rate_limit_exceeded", client.client_code)
            raise RateLimitExceededError(client.requests_per_minute)

    # ------------------------------------------------------------------
    # Standalone key check: lets the frontend confirm an API key is
    # valid/active/whitelisted right when it's entered, instead of only
    # finding out on the first real /autocheck submission. Reuses the
    # same stages 1-3 as the real pipeline so the result can never
    # diverge from what /autocheck itself would decide -- deliberately
    # skips stage 4 (rate limiting) so a validation ping never eats
    # into the client's actual request quota.
    # ------------------------------------------------------------------

    def validate_key(
        self,
        db: Session,
        api_key: str,
        client_ip: str,
    ) -> APIClient:
        client = self._validate_api_key(db, api_key, client_ip)
        self._check_client_status(client)
        self._check_ip_whitelist(db, client, client_ip)
        return client

    # ------------------------------------------------------------------
    # Pipeline stage 5: request logging.
    # ------------------------------------------------------------------

    def _log_request(
        self,
        db: Session,
        client: APIClient | None,
        client_ip: str,
        request_id: str,
        payload: AutoCheckRequest,
        response_status: int,
        elapsed_ms: int,
    ) -> None:
        """5. Request Logging.

        api_request_logs.client_id is a required FK, so a request that
        never resolved to a known client (invalid API key) can't be
        written here; that case is left to the application/access logs
        instead of the audit trail.
        """

        if client is None:
            return

        request_body = {
            "nationality": payload.passenger.nationality,
            "passport_type": payload.passenger.passport.type,
            "origin": payload.journey.origin,
            "destination": payload.journey.destination,
            "purpose": payload.journey.purpose,
            "travel_date": payload.journey.travel_date.isoformat(),
        }

        try:
            self.api_request_log_service.create_api_request_log(
                db,
                APIRequestLogCreate(
                    client_id=client.id,
                    ip_address=client_ip,
                    endpoint="/autocheck",
                    http_method=HTTPMethod.POST,
                    request_id=request_id,
                    request_body=request_body,
                    response_status=response_status,
                    response_time_ms=elapsed_ms,
                ),
            )
        except Exception:
            # Logging must never break the actual response to the caller.
            logger.exception("Failed to persist API request log.")

    # ------------------------------------------------------------------
    # Main entry point.
    # ------------------------------------------------------------------

    def run(
        self,
        db: Session,
        payload: AutoCheckRequest,
        client_ip: str,
        api_key: str,
    ) -> AutoCheckResponse:
        request_id = get_request_id()
        started_at = time.perf_counter()
        client: APIClient | None = None
        status_code = 200

        try:
            # 1. API Key Validation
            client = self._validate_api_key(db, api_key, client_ip)

            # 2. Client Status Check
            self._check_client_status(client)

            # 3. IP Whitelist Check
            self._check_ip_whitelist(db, client, client_ip)

            # 4. Rate Limiting (Redis)
            self._check_rate_limit(client)

            # 6. Rule Engine
            response = self._run_rule_engine(db, payload, client, request_id)

            return response

        except AppException as exc:
            status_code = exc.status_code
            raise
        except Exception:
            status_code = 500
            raise
        finally:
            elapsed_ms = max(1, round((time.perf_counter() - started_at) * 1000))
            # 5. Request Logging
            self._log_request(
                db,
                client,
                client_ip,
                request_id,
                payload,
                status_code,
                elapsed_ms,
            )

    # ------------------------------------------------------------------
    # Pipeline stage 6: Rule Engine -> Decision Generator -> persistence.
    # ------------------------------------------------------------------

    def _run_rule_engine(
        self,
        db: Session,
        payload: AutoCheckRequest,
        client: APIClient,
        request_id: str,
    ) -> AutoCheckResponse:
        engine = RuleEngine(db)

        stage_started_at = time.perf_counter()

        # --- Build the domain request from the API payload ---
        passport_in = payload.passenger.passport
        # issuing_country is optional on the request -- a passport issued
        # by the traveller's own nationality country is the common case,
        # so fall back to it when the field is left blank (matches the
        # help text shown on the autocheck form).
        issuing_country = passport_in.issuing_country or payload.passenger.nationality
        passenger = Passenger(
            nationality=payload.passenger.nationality,
            passport=PassportInfo(
                issuing_country=issuing_country,
                type=passport_in.type,
                valid_until=passport_in.valid_until,
                valid_from=passport_in.valid_from,
                blank_pages=passport_in.blank_pages,
            ),
            country_of_residence=payload.passenger.country_of_residence,
            existing_visas=[
                ExistingVisa(
                    type=v.type,
                    issuing_country=v.issuing_country,
                    valid_from=v.valid_from,
                    valid_until=v.valid_until,
                    entries=v.entries,
                )
                for v in payload.passenger.existing_visas
            ],
            passenger_type=payload.passenger.passenger_type,
            special_status=payload.passenger.special_status,
        )

        journey_in = payload.journey
        journey = Journey(
            origin=journey_in.origin,
            destination=journey_in.destination,
            travel_date=journey_in.travel_date,
            purpose=journey_in.purpose,
            return_date=journey_in.return_date,
            segments=[
                JourneySegment(
                    departure_airport=s.departure_airport,
                    arrival_airport=s.arrival_airport,
                    airline=s.airline,
                    flight_number=s.flight_number,
                    departure_datetime=s.departure_datetime,
                )
                for s in journey_in.segments
            ],
            transit_points=[
                TransitPoint(
                    airport=tp.airport,
                    duration_minutes=tp.duration_minutes,
                    requires_immigration=tp.requires_immigration,
                    separate_ticket=tp.separate_ticket,
                )
                for tp in journey_in.transit_points
            ],
        )

        # --- Single pipeline entry point: journey analysis, context,
        # rule loading, all 7 evaluators, run inside engine.execute() ---
        try:
            engine_result = engine.execute(
                JourneyRequest(passenger=passenger, journey=journey),
            )
        except ValueError as exc:
            raise UnknownReferenceDataError(str(exc)) from exc

        context = engine_result.context
        loaded_rules = engine_result.loaded_rules

        rule_rows_by_domain = {
            "visa": loaded_rules.visa_rule,
            "passport": loaded_rules.passport_rule,
            "health": loaded_rules.health_rule,
            "immigration": loaded_rules.immigration_rule,
            "customs": loaded_rules.customs_rule,
            "entry_restriction": loaded_rules.entry_restriction,
        }
        transit_rule_rows = [
            entry.transit_rule
            for entry in loaded_rules.transit_rules
            if entry.transit_rule is not None
        ]

        if all(row is None for row in rule_rows_by_domain.values()) and not transit_rule_rows:
            raise NoApplicableRulesError(
                payload.passenger.nationality,
                payload.journey.destination,
            )

        stage_elapsed_ms = max(
            1,
            round((time.perf_counter() - stage_started_at) * 1000),
        )

        # --- Save Rule Execution Logs + build provenance records ---
        # Note: rule_execution_logs.rule_id is a required FK to rules.id,
        # so we can only log a row for a domain where a stored rule was
        # actually found. A "no rule configured" domain has nothing to
        # point the FK at, so it's simply not logged here.
        execution_records: list[RuleExecutionRecord] = []

        def _log_match(domain: str, rule_row) -> None:
            reason = f"{domain} rule matched for this traveller."
            execution_records.append(
                RuleExecutionRecord(
                    rule_id=str(rule_row.rule_id),
                    rule_code=getattr(rule_row, "rule_code", "") or "",
                    domain=domain,
                    matched=True,
                    execution_time_ms=stage_elapsed_ms,
                    reason=reason,
                ),
            )
            self.rule_execution_log_service.create_rule_execution_log(
                db,
                RuleExecutionLogCreate(
                    request_id=request_id,
                    rule_id=rule_row.rule_id,
                    matched=True,
                    skipped=False,
                    execution_time_ms=stage_elapsed_ms,
                    reason=reason,
                ),
            )

        for domain, rule_row in rule_rows_by_domain.items():
            if rule_row is None:
                continue
            _log_match(domain, rule_row)

        for entry in loaded_rules.transit_rules:
            if entry.transit_rule is None:
                continue
            _log_match(f"transit ({entry.transit_point.country})", entry.transit_rule)

        # --- Resolve a rule_version for the compliance check ---
        # ComplianceCheck stores a single rule_version_id, but rules are
        # versioned per rule (per domain), not per compliance check. As a
        # simplification we attach the most recent version of the first
        # matched domain (visa first, since it's evaluated first/priority
        # in the decision), which is enough to trace which rule set
        # produced the decision, but is worth revisiting if compliance
        # checks need to reference every domain's version individually.
        rule_version = None

        for rule_row in list(rule_rows_by_domain.values()) + transit_rule_rows:
            if rule_row is None:
                continue

            rule_version = (
                db.query(RuleVersion)
                .filter(RuleVersion.rule_id == rule_row.rule_id)
                .order_by(RuleVersion.effective_date.desc())
                .first()
            )

            if rule_version is not None:
                break

        if rule_version is None:
            raise NoApplicableRulesError(
                payload.passenger.nationality,
                payload.journey.destination,
            )

        check_id = f"chk_{request_id}"

        # --- Decision Generator ---
        decision = engine.decision_generator.generate(
            engine_result=RuleEngineResult(
                requirements=engine_result.requirements,
                warnings=engine_result.warnings,
            ),
            context=context,
            rule_version=rule_version.version_number,
            check_id=check_id,
            execution_records=execution_records,
            journey_origin=payload.journey.origin,
            journey_destination=payload.journey.destination,
        )

        def _fmt(req: Requirement) -> str:
            return f"{req.title}: {req.details}" if req.details else req.title

        blockers = [
            _fmt(req)
            for req in decision.requirements
            if req.category == RequirementCategory.ENTRY_RESTRICTION
            and req.status == RequirementStatus.REQUIRED
        ]

        decision_enum = _STATUS_TO_DECISION.get(
            decision.decision,
            Decision.CONDITIONAL,
        )

        decision_reasons = (
            [{"type": "requirement", "text": _fmt(r)} for r in decision.requirements]
            + [{"type": "warning", "text": _fmt(r)} for r in decision.warnings]
            + [{"type": "blocker", "text": b} for b in blockers]
        )

        response_json = _json_safe(
            {
                "request": {
                    "nationality": payload.passenger.nationality,
                    "passport_type": payload.passenger.passport.type,
                    "origin": payload.journey.origin,
                    "destination": payload.journey.destination,
                    "purpose": payload.journey.purpose,
                    "travel_date": payload.journey.travel_date.isoformat(),
                },
                "decision": asdict(decision),
            }
        )

        input_hash = hashlib.sha256(
            json.dumps(
                {
                    "nationality": payload.passenger.nationality,
                    "passport_type": payload.passenger.passport.type,
                    "origin": payload.journey.origin,
                    "destination": payload.journey.destination,
                    "purpose": payload.journey.purpose,
                    "travel_date": payload.journey.travel_date.isoformat(),
                },
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()

        # --- Save Compliance Check ---
        compliance_check: ComplianceCheck = (
            self.compliance_check_service.create_compliance_check(
                db,
                ComplianceCheckCreate(
                    request_id=request_id,
                    client_id=client.id,
                    input_hash=input_hash,
                    rule_version_id=rule_version.id,
                    decision=decision_enum,
                    decision_reasons=decision_reasons,
                    response_json=response_json,
                ),
            )
        )

        # The flat per-domain fields below are a "primary detail card"
        # view for backward-compatible simple consumers -- they come
        # straight off the matched DB rows, not off the generic
        # requirements[] list. For a journey with multiple transit
        # points, only the FIRST transit point's rule is surfaced here;
        # the complete picture (every transit point independently) is
        # always in decision.requirements/warnings above.
        primary_transit_rule = transit_rule_rows[0] if transit_rule_rows else None

        return AutoCheckResponse(
            compliance_check_id=compliance_check.id,
            request_id=compliance_check.request_id,
            nationality=payload.passenger.nationality,
            origin=payload.journey.origin,
            destination=payload.journey.destination,
            purpose=payload.journey.purpose,
            passport_type=payload.passenger.passport.type,
            decision=ComplianceDecisionResponse(
                status=decision.decision.value,
                summary=decision.summary,
                requirements=[_fmt(r) for r in decision.requirements],
                warnings=[_fmt(r) for r in decision.warnings],
                blockers=blockers,
            ),
            visa=(
                VisaRequirementResponse.model_validate(loaded_rules.visa_rule)
                if loaded_rules.visa_rule
                else None
            ),
            passport=(
                PassportRequirementResponse.model_validate(loaded_rules.passport_rule)
                if loaded_rules.passport_rule
                else None
            ),
            transit=(
                TransitRequirementResponse.model_validate(primary_transit_rule)
                if primary_transit_rule
                else None
            ),
            health=(
                HealthRequirementResponse.model_validate(loaded_rules.health_rule)
                if loaded_rules.health_rule
                else None
            ),
            immigration=(
                ImmigrationRequirementResponse.model_validate(loaded_rules.immigration_rule)
                if loaded_rules.immigration_rule
                else None
            ),
            customs=(
                CustomsRequirementResponse.model_validate(loaded_rules.customs_rule)
                if loaded_rules.customs_rule
                else None
            ),
            entry_restriction=(
                EntryRestrictionResponse.model_validate(loaded_rules.entry_restriction)
                if loaded_rules.entry_restriction
                else None
            ),
        )