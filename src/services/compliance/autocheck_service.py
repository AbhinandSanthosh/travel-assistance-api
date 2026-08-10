import hashlib
import ipaddress
import json
import logging
import time
import uuid
from dataclasses import asdict
from datetime import date, datetime
from decimal import Decimal
from typing import Any

import redis
from sqlalchemy.orm import Session

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

# Maps the DecisionGenerator's free-text status onto the Decision enum
# stored on ComplianceCheck.decision.
_STATUS_TO_DECISION = {
    "COMPLIANT": Decision.ALLOWED,
    "ACTION_REQUIRED": Decision.CONDITIONAL,
    "ENTRY_RESTRICTED": Decision.NOT_ALLOWED,
}


def _json_safe(value: Any) -> Any:
    """Make dataclass output (Decimal, date) safe for a JSONB column."""

    def default(obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, date):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    return json.loads(json.dumps(value, default=default))


class AutoCheckService:
    """
    Orchestrates the full /autocheck request pipeline:

        1. API Key Validation
        2. Client Status Check
        3. IP Whitelist Check
        4. Rate Limiting (Redis)
        5. Request Logging
        6. Rule Engine (Journey Analyzer -> ... -> Decision Generator)
        7. Response

    This is the "Compliance Check Service" component from the project
    plan; the /autocheck endpoint itself stays a thin controller that
    just calls .run().
    """

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

    def _validate_api_key(self, db: Session, api_key: str) -> APIClient:
        """1. API Key Validation."""

        client = self.api_client_repository.get_by_api_key(db, api_key)

        if client is None:
            raise InvalidAPIKeyError()

        return client

    def _check_client_status(self, client: APIClient) -> None:
        """2. Client Status Check."""

        if not client.status:
            raise ClientInactiveError()

        if client.expires_at is not None:
            expires_at = client.expires_at
            now = (
                datetime.now(expires_at.tzinfo)
                if expires_at.tzinfo
                else datetime.utcnow()
            )

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
        client = self._validate_api_key(db, api_key)
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
            "nationality": payload.nationality,
            "origin": payload.origin,
            "destination": payload.destination,
            "purpose": payload.purpose,
            "passport_type": payload.passport_type,
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
        request_id = uuid.uuid4().hex
        started_at = time.perf_counter()
        client: APIClient | None = None
        status_code = 200

        try:
            # 1. API Key Validation
            client = self._validate_api_key(db, api_key)

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

        # --- Journey Analyzer / Context Builder / Rule Loader ---
        try:
            journey = engine.journey_analyzer.analyze(
                JourneyRequest(
                    nationality=payload.nationality,
                    destination=payload.destination,
                    purpose=payload.purpose,
                    passport_type=payload.passport_type,
                    origin=payload.origin,
                ),
            )
        except ValueError as exc:
            raise UnknownReferenceDataError(str(exc)) from exc

        context = engine.context_builder.build(
            journey=journey,
            travel_date=date.today(),
        )

        loaded_rules = engine.rule_loader.load(context)

        rule_rows_by_domain = {
            "visa": loaded_rules.visa_rule,
            "passport": loaded_rules.passport_rule,
            "transit": loaded_rules.transit_rule,
            "health": loaded_rules.health_rule,
            "immigration": loaded_rules.immigration_rule,
            "customs": loaded_rules.customs_rule,
            "entry_restriction": loaded_rules.entry_restriction,
        }

        if all(row is None for row in rule_rows_by_domain.values()):
            raise NoApplicableRulesError(
                payload.nationality,
                payload.destination,
            )

        # --- 7 Evaluators ---
        rule_engine_result = RuleEngineResult(
            visa=engine.visa_evaluator.evaluate(loaded_rules),
            passport=engine.passport_evaluator.evaluate(loaded_rules),
            transit=engine.transit_evaluator.evaluate(loaded_rules),
            health=engine.health_evaluator.evaluate(loaded_rules),
            immigration=engine.immigration_evaluator.evaluate(loaded_rules),
            customs=engine.customs_evaluator.evaluate(loaded_rules),
            entry_restriction=engine.entry_restriction_evaluator.evaluate(
                loaded_rules,
            ),
        )

        # --- Decision Generator ---
        decision = engine.decision_generator.generate(rule_engine_result)

        stage_elapsed_ms = max(
            1,
            round((time.perf_counter() - stage_started_at) * 1000),
        )

        # --- Save Rule Execution Logs ---
        # Note: rule_execution_logs.rule_id is a required FK to rules.id,
        # so we can only log a row for a domain where a stored rule was
        # actually found. A "no rule configured" domain has nothing to
        # point the FK at, so it's simply not logged here.
        for domain, rule_row in rule_rows_by_domain.items():
            if rule_row is None:
                continue

            self.rule_execution_log_service.create_rule_execution_log(
                db,
                RuleExecutionLogCreate(
                    request_id=request_id,
                    rule_id=rule_row.rule_id,
                    matched=True,
                    skipped=False,
                    execution_time_ms=stage_elapsed_ms,
                    reason=f"{domain} rule matched for this traveller.",
                ),
            )

        # --- Resolve a rule_version for the compliance check ---
        # ComplianceCheck stores a single rule_version_id, but rules are
        # versioned per rule (per domain), not per compliance check. As a
        # simplification we attach the most recent version of the first
        # matched domain (visa first, since it's evaluated first/priority
        # in the decision), which is enough to trace which rule set
        # produced the decision, but is worth revisiting if compliance
        # checks need to reference every domain's version individually.
        rule_version = None

        for rule_row in rule_rows_by_domain.values():
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
                payload.nationality,
                payload.destination,
            )

        decision_enum = _STATUS_TO_DECISION.get(
            decision.status,
            Decision.CONDITIONAL,
        )

        decision_reasons = (
            [{"type": "requirement", "text": text} for text in decision.requirements]
            + [{"type": "warning", "text": text} for text in decision.warnings]
            + [{"type": "blocker", "text": text} for text in decision.blockers]
        )

        response_json = _json_safe(
            {
                "request": {
                    "nationality": payload.nationality,
                    "origin": payload.origin,
                    "destination": payload.destination,
                    "purpose": payload.purpose,
                    "passport_type": payload.passport_type,
                },
                "decision": asdict(decision),
                "requirements": {
                    "visa": asdict(rule_engine_result.visa) if rule_engine_result.visa else None,
                    "passport": asdict(rule_engine_result.passport) if rule_engine_result.passport else None,
                    "transit": asdict(rule_engine_result.transit) if rule_engine_result.transit else None,
                    "health": asdict(rule_engine_result.health) if rule_engine_result.health else None,
                    "immigration": asdict(rule_engine_result.immigration) if rule_engine_result.immigration else None,
                    "customs": asdict(rule_engine_result.customs) if rule_engine_result.customs else None,
                    "entry_restriction": asdict(rule_engine_result.entry_restriction) if rule_engine_result.entry_restriction else None,
                },
            }
        )

        input_hash = hashlib.sha256(
            json.dumps(
                {
                    "nationality": payload.nationality,
                    "origin": payload.origin,
                    "destination": payload.destination,
                    "purpose": payload.purpose,
                    "passport_type": payload.passport_type,
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

        # --- 7. Response ---
        return AutoCheckResponse(
            compliance_check_id=compliance_check.id,
            request_id=compliance_check.request_id,
            nationality=payload.nationality,
            origin=payload.origin,
            destination=payload.destination,
            purpose=payload.purpose,
            passport_type=payload.passport_type,
            decision=ComplianceDecisionResponse.model_validate(decision),
            visa=(
                VisaRequirementResponse.model_validate(rule_engine_result.visa)
                if rule_engine_result.visa
                else None
            ),
            passport=(
                PassportRequirementResponse.model_validate(rule_engine_result.passport)
                if rule_engine_result.passport
                else None
            ),
            transit=(
                TransitRequirementResponse.model_validate(rule_engine_result.transit)
                if rule_engine_result.transit
                else None
            ),
            health=(
                HealthRequirementResponse.model_validate(rule_engine_result.health)
                if rule_engine_result.health
                else None
            ),
            immigration=(
                ImmigrationRequirementResponse.model_validate(rule_engine_result.immigration)
                if rule_engine_result.immigration
                else None
            ),
            customs=(
                CustomsRequirementResponse.model_validate(rule_engine_result.customs)
                if rule_engine_result.customs
                else None
            ),
            entry_restriction=(
                EntryRestrictionResponse.model_validate(rule_engine_result.entry_restriction)
                if rule_engine_result.entry_restriction
                else None
            ),
        )