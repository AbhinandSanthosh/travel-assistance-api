import hashlib
import ipaddress
import json
import logging
import time
import uuid
from dataclasses import asdict
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any

import redis
from sqlalchemy.orm import Session

from src.core.api_key import hash_api_key
from src.core.alerting import maybe_alert
from src.core.request_id import get_request_id
from src.domain.journey import (
    Journey,
    JourneySegment,
    TransitPoint,
)
from src.domain.passenger import (
    ExistingVisa,
    Passenger,
    PassportInfo,
)
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
from src.models.rule_management.rule_version import (
    RuleVersion,
)
from src.repositories.administration.api_client import (
    APIClientRepository,
)
from src.rule_engine.decision_generator import (
    DecisionGenerator,
)
from src.rule_engine.engine import RuleEngine
from src.rule_engine.models import JourneyRequest
from src.schemas.administration.api_request_log import (
    APIRequestLogCreate,
)
from src.schemas.compliance.compliance_check import (
    ComplianceCheckCreate,
)
from src.schemas.compliance.rule_execution_log import (
    RuleExecutionLogCreate,
)
from src.schemas.v1.travel_requirements import (
    JourneySummaryResponse,
    RequirementResponse,
    RuleExecutionResponse,
    SubRequirementResponse,
    TravelRequirementsCheckRequest,
    TravelRequirementsCheckResponse,
)
from src.services.administration.api_request_log import (
    APIRequestLogService,
)
from src.services.administration.client_ip_whitelist import (
    ClientIPWhitelistService,
)
from src.services.compliance.compliance_check import (
    ComplianceCheckService,
)
from src.services.compliance.rule_execution_log import (
    RuleExecutionLogService,
)


logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #

_DECISION_MAP = {
    "CLEAR": Decision.ALLOWED,
    "ACTION_REQUIRED": Decision.CONDITIONAL,
    "NOT_PERMITTED": Decision.NOT_ALLOWED,
    "CONDITIONAL": Decision.CONDITIONAL,
    "UNKNOWN": Decision.NOT_ALLOWED,
}


def _json_safe(value: Any) -> Any:
    """Make dataclass output safe for a JSONB column."""

    def default(obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if hasattr(obj, "value"):
            return obj.value
        raise TypeError(
            f"Object of type {type(obj).__name__} "
            f"is not JSON serializable"
        )

    return json.loads(json.dumps(value, default=default))


def _to_passenger(p) -> Passenger:
    return Passenger(
        nationality=p.nationality,
        passport=PassportInfo(
            issuing_country=p.passport.country,
            type=p.passport.type,
            valid_until=p.passport.valid_until,
            valid_from=p.passport.valid_from,
            blank_pages=p.passport.blank_pages,
        ),
        country_of_residence=p.country_of_residence,
        existing_visas=[
            ExistingVisa(
                type=v.type,
                issuing_country=v.issuing_country,
                valid_from=v.valid_from,
                valid_until=v.valid_until,
                entries=v.entries,
            )
            for v in p.existing_visas
        ],
        passenger_type=p.passenger_type,
        special_status=p.special_status,
    )


def _to_journey(j) -> Journey:
    return Journey(
        origin=j.origin,
        destination=j.destination,
        travel_date=j.travel_date,
        purpose=j.purpose,
        return_date=j.return_date,
        segments=[
            JourneySegment(
                departure_airport=s.departure_airport,
                arrival_airport=s.arrival_airport,
                airline=s.airline,
                flight_number=s.flight_number,
                departure_datetime=s.departure_datetime,
            )
            for s in j.segments
        ],
        transit_points=[
            TransitPoint(
                airport=tp.airport,
                duration_minutes=tp.duration_minutes,
                requires_immigration=tp.requires_immigration,
                separate_ticket=tp.separate_ticket,
            )
            for tp in j.transit_points
        ],
    )


def _requirement_to_response(r) -> RequirementResponse:
    return RequirementResponse(
        category=(
            r.category.value
            if hasattr(r.category, "value")
            else r.category
        ),
        status=(
            r.status.value
            if hasattr(r.status, "value")
            else r.status
        ),
        title=r.title,
        details=r.details,
        sub_requirements=[
            SubRequirementResponse(
                type=s.type,
                name=s.name,
                status=(
                    s.status.value
                    if hasattr(s.status, "value")
                    else s.status
                ),
                details=s.details,
            )
            for s in r.sub_requirements
        ],
        applicable_rule=r.applicable_rule_id,
        applicable_rule_code=r.applicable_rule_code,
        source=r.source,
        effective_from=r.effective_from,
        effective_until=r.effective_until,
    )


def _build_response(
    decision,
    domains: list[str] | None = None,
) -> TravelRequirementsCheckResponse:

    reqs = decision.requirements
    warns = decision.warnings

    if domains:
        reqs = [
            r
            for r in reqs
            if (
                r.category.value
                if hasattr(r.category, "value")
                else r.category
            )
            in domains
        ]
        warns = [
            w
            for w in warns
            if (
                w.category.value
                if hasattr(w.category, "value")
                else w.category
            )
            in domains
        ]

    return TravelRequirementsCheckResponse(
        check_id=decision.check_id,
        decision=(
            decision.decision.value
            if hasattr(decision.decision, "value")
            else decision.decision
        ),
        summary=decision.summary,
        requirements=[
            _requirement_to_response(r) for r in reqs
        ],
        warnings=[
            _requirement_to_response(w) for w in warns
        ],
        journey=JourneySummaryResponse(
            origin=decision.journey.origin,
            destination=decision.journey.destination,
            transit_countries=(
                decision.journey.transit_countries
            ),
        ),
        rule_execution_log=[
            RuleExecutionResponse(
                rule_id=r.rule_id,
                rule_code=r.rule_code,
                domain=r.domain,
                matched=r.matched,
                reason=r.reason,
            )
            for r in decision.rule_execution_log
        ],
        evaluated_at=decision.evaluated_at,
        rule_version=decision.rule_version,
    )


# ------------------------------------------------------------------ #
# Service
# ------------------------------------------------------------------ #


class TravelRequirementsService:
    """TISCO v1 service: API pipeline + rule engine + persistence."""

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
        self.client_ip_whitelist_service = (
            client_ip_whitelist_service
        )
        self.api_request_log_service = (
            api_request_log_service
        )
        self.compliance_check_service = (
            compliance_check_service
        )
        self.rule_execution_log_service = (
            rule_execution_log_service
        )
        self.redis_client = redis_client

    # -------------------------------------------------------------- #
    # Pipeline stages 1-4 (identical to AutoCheckService)
    # -------------------------------------------------------------- #

    def _validate_api_key(
        self,
        db: Session,
        api_key: str,
        client_ip: str,
    ) -> APIClient:

        client = (
            self.api_client_repository.get_by_api_key_hash(
                db,
                hash_api_key(api_key),
            )
        )

        if client is None:
            client = (
                self.api_client_repository.get_by_api_key(
                    db, api_key,
                )
            )

        if client is None:
            maybe_alert("invalid_api_key", client_ip)
            raise InvalidAPIKeyError()

        return client

    def _check_client_status(
        self, client: APIClient,
    ) -> None:

        if not client.status:
            raise ClientInactiveError()

        if client.expires_at is not None:
            expires_at = client.expires_at
            if expires_at.tzinfo is not None:
                expires_at = expires_at.astimezone(
                    timezone.utc,
                ).replace(tzinfo=None)

            now = datetime.now(timezone.utc).replace(
                tzinfo=None,
            )

            if expires_at < now:
                raise ClientExpiredError(
                    expires_at.isoformat(),
                )

    def _check_ip_whitelist(
        self,
        db: Session,
        client: APIClient,
        client_ip: str,
    ) -> None:

        entries = self.client_ip_whitelist_service.get_client_whitelist_entries(
            db,
            client.id,
        )
        active_entries = [
            entry for entry in entries if entry.active
        ]

        if not active_entries:
            return

        try:
            ip_obj = ipaddress.ip_address(client_ip)
        except ValueError:
            maybe_alert(
                "ip_whitelist_rejected",
                client_ip,
                {"client_code": client.client_code},
            )
            raise IPNotWhitelistedError(
                client_ip,
            ) from None

        for entry in active_entries:
            if (
                entry.ip_address
                and entry.ip_address == client_ip
            ):
                return

            if entry.cidr_range:
                try:
                    network = ipaddress.ip_network(
                        entry.cidr_range,
                        strict=False,
                    )
                except ValueError:
                    continue

                if ip_obj in network:
                    return

        maybe_alert(
            "ip_whitelist_rejected",
            client_ip,
            {"client_code": client.client_code},
        )
        raise IPNotWhitelistedError(client_ip)

    def _check_rate_limit(
        self, client: APIClient,
    ) -> None:

        window = int(time.time() // 60)
        key = (
            f"ratelimit:travel_requirements:"
            f"{client.id}:{window}"
        )

        try:
            current = self.redis_client.incr(key)
            if current == 1:
                self.redis_client.expire(key, 60)
        except redis.exceptions.RedisError as exc:
            logger.warning(
                "Rate limiting unavailable (%s); "
                "allowing request.",
                exc,
            )
            return

        if current > client.requests_per_minute:
            maybe_alert(
                "rate_limit_exceeded",
                client.client_code,
            )
            raise RateLimitExceededError(
                client.requests_per_minute,
            )

    # -------------------------------------------------------------- #
    # Request logging
    # -------------------------------------------------------------- #

    def _log_request(
        self,
        db: Session,
        client: APIClient | None,
        client_ip: str,
        request_id: str,
        payload: TravelRequirementsCheckRequest,
        response_status: int,
        elapsed_ms: int,
    ) -> None:

        if client is None:
            return

        request_body = {
            "nationality": payload.passenger.nationality,
            "origin": payload.journey.origin,
            "destination": payload.journey.destination,
            "purpose": payload.journey.purpose,
            "passport_type": payload.passenger.passport.type,
        }

        try:
            self.api_request_log_service.create_api_request_log(
                db,
                APIRequestLogCreate(
                    client_id=client.id,
                    ip_address=client_ip,
                    endpoint="/api/v1/travel-requirements/check",
                    http_method=HTTPMethod.POST,
                    request_id=request_id,
                    request_body=request_body,
                    response_status=response_status,
                    response_time_ms=elapsed_ms,
                ),
            )
        except Exception:
            logger.exception(
                "Failed to persist API request log.",
            )

    # -------------------------------------------------------------- #
    # Main entry point
    # -------------------------------------------------------------- #

    def check(
        self,
        db: Session,
        payload: TravelRequirementsCheckRequest,
        client_ip: str,
        api_key: str,
        domains: list[str] | None = None,
    ) -> TravelRequirementsCheckResponse:

        request_id = get_request_id()
        started_at = time.perf_counter()
        client: APIClient | None = None
        status_code = 200

        try:
            # 1. API Key Validation
            client = self._validate_api_key(
                db, api_key, client_ip,
            )

            # 2. Client Status Check
            self._check_client_status(client)

            # 3. IP Whitelist Check
            self._check_ip_whitelist(
                db, client, client_ip,
            )

            # 4. Rate Limiting
            self._check_rate_limit(client)

            # 5. Rule Engine
            return self._run_engine(
                db,
                payload,
                client,
                request_id,
                domains,
            )

        except AppException as exc:
            status_code = exc.status_code
            raise
        except Exception:
            status_code = 500
            raise
        finally:
            elapsed_ms = max(
                1,
                round(
                    (time.perf_counter() - started_at)
                    * 1000
                ),
            )
            self._log_request(
                db,
                client,
                client_ip,
                request_id,
                payload,
                status_code,
                elapsed_ms,
            )

    # -------------------------------------------------------------- #
    # Rule Engine → Decision → Persistence
    # -------------------------------------------------------------- #

    def _run_engine(
        self,
        db: Session,
        payload: TravelRequirementsCheckRequest,
        client: APIClient,
        request_id: str,
        domains: list[str] | None,
    ) -> TravelRequirementsCheckResponse:

        engine = RuleEngine(db)
        stage_started_at = time.perf_counter()

        # --- Convert Pydantic → Domain ---
        passenger = _to_passenger(payload.passenger)
        journey = _to_journey(payload.journey)

        # --- Execute Rule Engine ---
        try:
            engine_result = engine.execute(
                JourneyRequest(
                    passenger=passenger,
                    journey=journey,
                ),
            )
        except ValueError as exc:
            raise UnknownReferenceDataError(
                str(exc),
            ) from exc

        stage_elapsed_ms = max(
            1,
            round(
                (time.perf_counter() - stage_started_at)
                * 1000
            ),
        )

        # --- Resolve rule_version ---
        rule_version = (
            db.query(RuleVersion)
            .order_by(RuleVersion.effective_date.desc())
            .first()
        )

        if rule_version is None:
            raise NoApplicableRulesError(
                payload.passenger.nationality,
                payload.journey.destination,
            )

        # --- Build context (once) for decision generation ---
        jr = JourneyRequest(
            passenger=passenger,
            journey=journey,
        )
        analyzed = engine.journey_analyzer.analyze(jr)
        context = engine.context_builder.build(
            journey=analyzed,
            passenger=passenger,
        )

        # --- Generate Decision ---
        check_id = f"chk_{uuid.uuid4().hex[:24]}"
        decision_generator = DecisionGenerator()

        decision = decision_generator.generate(
            engine_result=engine_result,
            context=context,
            rule_version=str(rule_version.version),
            check_id=check_id,
            journey_origin=payload.journey.origin,
            journey_destination=(
                payload.journey.destination
            ),
        )

        # --- Persist Compliance Check ---
        decision_value = (
            decision.decision.value
            if hasattr(decision.decision, "value")
            else str(decision.decision)
        )
        decision_enum = _DECISION_MAP.get(
            decision_value,
            Decision.NOT_ALLOWED,
        )

        decision_reasons = [
            {"type": "requirement", "text": r.title}
            for r in decision.requirements
            if r.status.value
            in ("REQUIRED", "CONDITIONAL", "UNKNOWN")
        ] + [
            {"type": "warning", "text": w.title}
            for w in decision.warnings
        ]

        response_json = _json_safe(asdict(decision))

        input_hash = hashlib.sha256(
            json.dumps(
                {
                    "nationality": (
                        payload.passenger.nationality
                    ),
                    "origin": payload.journey.origin,
                    "destination": (
                        payload.journey.destination
                    ),
                    "purpose": payload.journey.purpose,
                    "passport_type": (
                        payload.passenger.passport.type
                    ),
                },
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()

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

        # --- Persist Rule Execution Logs ---
        # rule_execution_logs.rule_id is a required FK to
        # rules.id. We derive rule_ids from the requirements
        # the engine already produced (no redundant queries).

        # Simplified: log once for the first matched rule
        for domain in [
            "visa",
            "passport",
            "health",
            "immigration",
            "customs",
            "entry_restriction",
        ]:
            # We already have engine_result requirements
            # Use the first requirement with an applicable
            # rule_id that points to a real rule
            for req in (
                engine_result.requirements
                + engine_result.warnings
            ):
                if (
                    req.applicable_rule_id
                    and req.category.value.upper()
                    == domain.upper()
                ):
                    try:
                        rule_id = int(
                            req.applicable_rule_id,
                        )
                    except (ValueError, TypeError):
                        continue

                    try:
                        self.rule_execution_log_service.create_rule_execution_log(
                            db,
                            RuleExecutionLogCreate(
                                request_id=request_id,
                                rule_id=rule_id,
                                matched=True,
                                skipped=False,
                                execution_time_ms=(
                                    stage_elapsed_ms
                                ),
                                reason=(
                                    f"{domain} rule "
                                    f"matched."
                                ),
                            ),
                        )
                    except Exception:
                        logger.exception(
                            "Failed to persist rule "
                            "execution log for %s.",
                            domain,
                        )
                    break

        return _build_response(decision, domains)
