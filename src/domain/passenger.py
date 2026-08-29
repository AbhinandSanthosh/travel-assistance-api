

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class PassportInfo:
    """Passport details carried by the passenger."""

    issuing_country: str          # ISO 3166-1 alpha-2
    type: str                     # ORDINARY, DIPLOMATIC, SERVICE, EMERGENCY, etc.
    valid_until: date
    valid_from: date | None = None
    blank_pages: int | None = None


@dataclass
class ExistingVisa:
    """A visa the passenger already holds.

    The rule engine uses this to determine whether a visa requirement
    is already satisfied (e.g. passenger holds a valid Schengen visa
    and is transiting through a Schengen country).
    """

    type: str                     # e.g. SCHENGEN, TOURIST, WORK
    issuing_country: str          # ISO alpha-2
    valid_from: date | None = None
    valid_until: date | None = None
    entries: str | None = None    # SINGLE, MULTIPLE, UNLIMITED


@dataclass
class Passenger:
    """Complete passenger profile submitted with a check request.

    Attributes:
        nationality: ISO alpha-2 country code of the passenger's
            citizenship.
        passport: Passport the passenger will travel on.
        country_of_residence: ISO alpha-2 code of the country where the
            passenger currently resides (may differ from nationality and
            can affect visa/entry requirements).
        existing_visas: Visas the passenger already holds that may
            satisfy destination or transit requirements.
        passenger_type: ADULT, CHILD, INFANT, or CREW. Some rules
            differ by passenger type (e.g. unaccompanied minors).
        special_status: DIPLOMAT, REFUGEE, STATELESS, SEAMAN, MILITARY,
            or None. Certain immigration statuses grant exemptions from
            standard visa/entry requirements.
    """

    nationality: str
    passport: PassportInfo
    country_of_residence: str | None = None
    existing_visas: list[ExistingVisa] = field(default_factory=list)
    passenger_type: str | None = None
    special_status: str | None = None
