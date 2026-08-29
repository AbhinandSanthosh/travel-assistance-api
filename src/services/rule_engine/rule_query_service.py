from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import Query, Session, joinedload

from src.models.compliance.customs_rule import CustomsRule
from src.models.compliance.entry_restriction import EntryRestriction
from src.models.compliance.health_rule import HealthRule
from src.models.compliance.health_rule_vaccine import HealthRuleVaccine
from src.models.compliance.immigration_rule import ImmigrationRule
from src.models.compliance.passport_rule import PassportRule
from src.models.compliance.rule import Rule
from src.models.compliance.transit_rule import TransitRule
from src.models.compliance.visa_rule import VisaRule
from src.models.rule_management.rule_status import RuleStatus
from src.models.rule_management.rule_version import RuleVersion

# NOTE: no rule_statuses rows are seeded by the initial migration --
# they're created via the admin rule-status API. "PUBLISHED" is the
# code this filter expects a rule to have before the engine will ever
# resolve it (matching the mentor-specified query pattern) -- if your
# seeded value differs, update this one constant.
PUBLISHED_STATUS_CODE = "PUBLISHED"


class RuleQueryService:
    """
    Read-only queries used by the Rule Engine.

    Every query here enforces three things a raw `.filter(...).first()`
    on the domain table alone does NOT: the rule must be PUBLISHED (not
    a draft or a rule pending approval), its version must actually be
    in effect on the travel date (not before effective_date, not after
    expiry_date), and when more than one rule matches, the
    highest-priority one wins. Skipping any of these means the engine
    could return a stale, unapproved, or superseded rule.
    """

    def __init__(self, db: Session):
        self.db = db

    def _active_version_filter(self, query: Query, model, travel_date: date) -> Query:
        """Join onto Rule/RuleVersion/RuleStatus and constrain to a
        PUBLISHED rule whose version is in effect on travel_date,
        highest priority first. `query` must already be filtered down
        to a specific rule table (VisaRule, PassportRule, etc.); `model`
        is that same table's class (must have a `rule_id` column) --
        this only adds the status/date/priority layer on top.
        """

        return (
            query.join(Rule, Rule.id == model.rule_id)
            .join(RuleVersion, RuleVersion.rule_id == Rule.id)
            .join(RuleStatus, RuleStatus.id == Rule.status_id)
            .filter(
                RuleStatus.status_code == PUBLISHED_STATUS_CODE,
                RuleVersion.effective_date <= travel_date,
                or_(
                    RuleVersion.expiry_date.is_(None),
                    RuleVersion.expiry_date >= travel_date,
                ),
            )
            .order_by(Rule.priority.desc())
        )

    def get_visa_rule(
        self,
        nationality_country_id: int,
        destination_country_id: int,
        passport_type_id: int,
        purpose_id: int,
        travel_date: date,
    ) -> VisaRule | None:
        """
        Retrieve the applicable, currently-in-effect visa rule.
        """

        query = self.db.query(VisaRule).filter(
            VisaRule.nationality_country_id == nationality_country_id,
            VisaRule.destination_country_id == destination_country_id,
            VisaRule.passport_type_id == passport_type_id,
            VisaRule.purpose_id == purpose_id,
        )
        return self._active_version_filter(query, VisaRule, travel_date).first()

    def get_passport_rule(
        self,
        nationality_country_id: int,
        destination_country_id: int,
        passport_type_id: int,
        travel_date: date,
    ) -> PassportRule | None:
        """
        Retrieve the applicable, currently-in-effect passport rule.
        """

        query = self.db.query(PassportRule).filter(
            PassportRule.destination_country_id == destination_country_id,
            PassportRule.passport_type_id == passport_type_id,
        )
        return self._active_version_filter(query, PassportRule, travel_date).first()

    def get_transit_rule(
        self,
        nationality_country_id: int,
        transit_country_id: int,
        transit_airport_id: int,
        travel_date: date,
    ) -> TransitRule | None:
        """
        Retrieve the applicable, currently-in-effect transit rule.
        """

        query = self.db.query(TransitRule).filter(
            TransitRule.nationality_country_id == nationality_country_id,
            TransitRule.transit_country_id == transit_country_id,
            TransitRule.transit_airport_id == transit_airport_id,
        )
        return self._active_version_filter(query, TransitRule, travel_date).first()

    def get_health_rule(
        self,
        nationality_country_id: int,
        destination_country_id: int,
        travel_date: date,
        origin_country_id: int | None = None,
    ) -> HealthRule | None:
        """
        Retrieve the applicable, currently-in-effect health rule
        together with its associated vaccines.

        Health requirements (e.g. Yellow Fever certificates) can depend
        on the traveller's point of departure, not just nationality —
        an Indian national flying to Poland via a Yellow-Fever-risk
        country needs different handling than one flying direct. When an
        origin is supplied, an origin-specific rule takes priority; if
        none exists, this falls back to the origin-agnostic rule (the
        row with origin_country_id IS NULL) so existing data keeps
        working unchanged.
        """

        base_query = (
            self.db.query(HealthRule)
            .options(
                joinedload(HealthRule.health_rule_vaccines).joinedload(
                    HealthRuleVaccine.vaccine
                )
            )
            .filter(
                HealthRule.nationality_country_id == nationality_country_id,
                HealthRule.destination_country_id == destination_country_id,
            )
        )
        base_query = self._active_version_filter(base_query, HealthRule, travel_date)

        if origin_country_id is not None:
            origin_specific = base_query.filter(
                HealthRule.origin_country_id == origin_country_id,
            ).first()

            if origin_specific is not None:
                return origin_specific

        return base_query.filter(
            HealthRule.origin_country_id.is_(None),
        ).first()

    def get_immigration_rule(
        self,
        destination_country_id: int,
        travel_date: date,
    ) -> ImmigrationRule | None:
        """
        Retrieve the applicable, currently-in-effect immigration rule.
        """

        query = self.db.query(ImmigrationRule).filter(
            ImmigrationRule.destination_country_id == destination_country_id,
        )
        return self._active_version_filter(query, ImmigrationRule, travel_date).first()

    def get_customs_rule(
        self,
        nationality_country_id: int,
        destination_country_id: int,
        travel_date: date,
    ) -> CustomsRule | None:
        """
        Retrieve the applicable, currently-in-effect customs rule.
        """

        query = (
            self.db.query(CustomsRule)
            .options(joinedload(CustomsRule.currency))
            .filter(
                CustomsRule.nationality_country_id == nationality_country_id,
                CustomsRule.destination_country_id == destination_country_id,
            )
        )
        return self._active_version_filter(query, CustomsRule, travel_date).first()

    def get_entry_restriction(
        self,
        nationality_country_id: int,
        destination_country_id: int,
        travel_date: date,
        origin_country_id: int | None = None,
    ) -> EntryRestriction | None:
        """
        Retrieve the applicable, currently-in-effect entry restriction.

        Same origin-aware matching as get_health_rule: an origin-specific
        restriction (e.g. a route-based ban tied to the embarkation
        country) is preferred over the origin-agnostic one when both the
        origin is known and a matching row exists.

        Effective/expiry dates matter especially here: an entry
        restriction that hasn't started yet, or has already lapsed,
        must never be treated as currently blocking.
        """

        base_query = (
            self.db.query(EntryRestriction)
            .options(joinedload(EntryRestriction.source))
            .filter(
                EntryRestriction.nationality_country_id == nationality_country_id,
                EntryRestriction.destination_country_id == destination_country_id,
            )
        )
        base_query = self._active_version_filter(base_query, EntryRestriction, travel_date)

        if origin_country_id is not None:
            origin_specific = base_query.filter(
                EntryRestriction.origin_country_id == origin_country_id,
            ).first()

            if origin_specific is not None:
                return origin_specific

        return base_query.filter(
            EntryRestriction.origin_country_id.is_(None),
        ).first()
