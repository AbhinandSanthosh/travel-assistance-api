"""
Decision and requirement models for the TISCO Decision Engine.

Defines the expanded decision statuses, per-requirement statuses,
requirement categories, and the structured output types that make
the API response consumable by booking systems and frontends.

Key design decisions:
- UNKNOWN is a first-class status: a compliance system must never
  silently turn missing regulatory data into "allowed."
- Each requirement carries its own provenance (rule ID, source,
  effective dates) for full auditability.
- Sub-requirements allow structured nesting (e.g. individual
  vaccines within a HEALTH requirement).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum


# ------------------------------------------------------------------ #
# Decision-level status (overall journey verdict)
# ------------------------------------------------------------------ #

class DecisionStatus(str, Enum):
    """Overall decision for a travel requirements check.

    CLEAR           – passenger meets all requirements, no action needed.
    ACTION_REQUIRED – one or more requirements must be fulfilled.
    NOT_PERMITTED   – travel is not permitted (entry restriction, ban).
    CONDITIONAL     – travel may be possible subject to conditions.
    UNKNOWN         – insufficient regulatory data to make a determination.
    """

    CLEAR = "CLEAR"
    ACTION_REQUIRED = "ACTION_REQUIRED"
    NOT_PERMITTED = "NOT_PERMITTED"
    CONDITIONAL = "CONDITIONAL"
    UNKNOWN = "UNKNOWN"


# ------------------------------------------------------------------ #
# Per-requirement status
# ------------------------------------------------------------------ #

class RequirementStatus(str, Enum):
    """Status of an individual requirement within the decision."""

    REQUIRED = "REQUIRED"
    NOT_REQUIRED = "NOT_REQUIRED"
    RECOMMENDED = "RECOMMENDED"
    CONDITIONAL = "CONDITIONAL"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNKNOWN = "UNKNOWN"


# ------------------------------------------------------------------ #
# Requirement categories (rule domains)
# ------------------------------------------------------------------ #

class RequirementCategory(str, Enum):
    """The compliance domain a requirement belongs to."""

    VISA = "VISA"
    PASSPORT = "PASSPORT"
    TRANSIT = "TRANSIT"
    HEALTH = "HEALTH"
    IMMIGRATION = "IMMIGRATION"
    CUSTOMS = "CUSTOMS"
    ENTRY_RESTRICTION = "ENTRY_RESTRICTION"


# ------------------------------------------------------------------ #
# Structured requirement output
# ------------------------------------------------------------------ #

@dataclass
class SubRequirement:
    """A nested requirement within a parent (e.g. a specific vaccine).

    Attributes:
        type: Discriminator (VACCINATION, CERTIFICATE, DECLARATION, etc.)
        name: Human-readable name of the specific item.
        status: Whether this sub-item is required/recommended/etc.
        details: Free-text explanation.
    """

    type: str
    name: str
    status: RequirementStatus
    details: str | None = None


@dataclass
class Requirement:
    """A single travel requirement returned by the engine.

    Each requirement carries enough metadata for the consumer to
    understand what is needed, why, and where the rule came from.

    Attributes:
        category: Which compliance domain (VISA, PASSPORT, etc.)
        status: Whether this requirement is REQUIRED, RECOMMENDED, etc.
        title: Short human-readable title.
        details: Longer explanation with actionable information.
        sub_requirements: Nested items (e.g. individual vaccines).
        applicable_rule_id: DB ID of the matched rule (for audit).
        applicable_rule_code: Human-readable rule code (e.g. VISA-DE-IN-TOUR-42).
        source: Name of the authority/source that published the rule.
        effective_from: When the rule became/becomes effective.
        effective_until: When the rule expires (None = indefinite).
    """

    category: RequirementCategory
    status: RequirementStatus
    title: str
    details: str
    sub_requirements: list[SubRequirement] = field(default_factory=list)
    applicable_rule_id: str | None = None
    applicable_rule_code: str | None = None
    source: str | None = None
    effective_from: date | None = None
    effective_until: date | None = None


# ------------------------------------------------------------------ #
# Provenance / execution logging
# ------------------------------------------------------------------ #

@dataclass
class RuleExecutionRecord:
    """Record of a single rule evaluation for provenance/audit.

    Captured during engine execution and included in the response
    so consumers can trace exactly which rules produced the decision.
    """

    rule_id: str
    rule_code: str
    domain: str
    matched: bool
    execution_time_ms: int
    reason: str | None = None
    source_document: str | None = None
    document_version: str | None = None


# ------------------------------------------------------------------ #
# Journey summary (echoed in response)
# ------------------------------------------------------------------ #

@dataclass
class JourneySummary:
    """Simplified journey echo included in the response."""

    origin: str
    destination: str
    transit_countries: list[str] = field(default_factory=list)


# ------------------------------------------------------------------ #
# Top-level decision container
# ------------------------------------------------------------------ #

@dataclass
class TravelRequirementsDecision:
    """Complete decision returned by the TISCO Decision Engine.

    This is the canonical output of a travel requirements check,
    containing the overall verdict, all individual requirements and
    warnings, journey summary, and the full execution provenance.
    """

    check_id: str
    decision: DecisionStatus
    summary: str
    requirements: list[Requirement]
    warnings: list[Requirement]
    journey: JourneySummary
    rule_execution_log: list[RuleExecutionRecord]
    evaluated_at: datetime
    rule_version: str
