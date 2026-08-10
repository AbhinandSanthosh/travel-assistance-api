"""
Auto Check view: submits a traveller's details to POST /autocheck and
renders the compliance decision plus the full per-category travel
requirement breakdown. Uses the same APIClient/APIError conventions as
the rest of the console.
"""

import streamlit as st

from api_client import APIError

# st.dialog was renamed from st.experimental_dialog in Streamlit 1.37;
# support either so this works across the >=1.35 range pinned in
# requirements.txt.
_dialog = getattr(st, "dialog", None) or st.experimental_dialog

DEFAULT_API_KEY = "demo_api_key_123456789"

FALLBACK_COUNTRIES = ["India", "Poland", "Saudi Arabia"]
FALLBACK_PURPOSES = [
    ("TOUR", "Tourism"),
    ("BUSINESS", "Business"),
    ("STUDY", "Study"),
    ("WORK", "Employment"),
    ("MEDICAL", "Medical"),
]
FALLBACK_PASSPORT_TYPES = [("PP", "Ordinary Passport")]

STATUS_DISPLAY = {
    "COMPLIANT": ("Compliant", "success"),
    "ACTION_REQUIRED": ("Action Required", "warning"),
    "ENTRY_RESTRICTED": ("Entry Restricted", "error"),
}

DOMAIN_LABELS = {
    "visa": {
        "visa_required": "Visa required",
        "visa_type": "Visa type",
        "visa_on_arrival": "Visa on arrival",
        "evisa_available": "e-Visa available",
        "max_stay_days": "Maximum stay (days)",
        "multiple_entry": "Multiple entry",
        "remarks": "Remarks",
    },
    "passport": {
        "minimum_validity_months": "Minimum validity (months)",
        "blank_pages_required": "Blank pages required",
        "machine_readable_required": "Machine readable required",
        "damaged_passport_allowed": "Damaged passport allowed",
        "temporary_passport_allowed": "Temporary passport allowed",
        "passport_issue_date_required": "Issue date required",
        "remarks": "Remarks",
    },
    "transit": {
        "transit_visa_required": "Transit visa required",
        "airside_transit_allowed": "Airside transit allowed",
        "baggage_collection_required": "Baggage collection required",
        "overnight_transit_allowed": "Overnight transit allowed",
        "max_transit_hours": "Maximum transit hours",
        "remarks": "Remarks",
    },
    "health": {
        "health_form_required": "Health form required",
        "quarantine_required": "Quarantine required",
        "quarantine_days": "Quarantine days",
        "medical_certificate_required": "Medical certificate required",
        "remarks": "Remarks",
    },
    "immigration": {
        "onward_ticket_required": "Onward ticket required",
        "accommodation_proof_required": "Accommodation proof required",
        "proof_of_funds_required": "Proof of funds required",
        "biometric_required": "Biometric verification required",
        "interview_required": "Interview required",
        "arrival_card_required": "Arrival card required",
        "digital_arrival_card": "Digital arrival card",
        "arrival_registration_required": "Arrival registration required",
        "remarks": "Remarks",
    },
    "customs": {
        "alcohol_limit": "Alcohol limit",
        "tobacco_limit": "Tobacco limit",
        "currency_limit_amount": "Currency limit amount",
        "currency": "Currency",
        "currency_declaration_required": "Currency declaration required",
        "medication_rules": "Medication rules",
        "prohibited_items": "Prohibited items",
        "restricted_items": "Restricted items",
        "pet_import_rules": "Pet import rules",
        "remarks": "Remarks",
    },
    "entry_restriction": {
        "restriction_type": "Restriction type",
        "reason": "Reason",
        "effective_date": "Effective date",
        "expiry_date": "Expiry date",
        "source": "Source",
        "remarks": "Remarks",
    },
}

DOMAIN_TABS = [
    ("Visa", "visa"),
    ("Passport", "passport"),
    ("Transit", "transit"),
    ("Health", "health"),
    ("Immigration", "immigration"),
    ("Customs", "customs"),
    ("Entry Restriction", "entry_restriction"),
]


def _load_reference_data(client):
    if "autocheck_reference" in st.session_state:
        return st.session_state["autocheck_reference"]

    def _safe_list(path):
        try:
            return client.list(path)
        except (APIError, Exception):
            return None

    countries = _safe_list("/countries")
    purposes = _safe_list("/purposes")
    passport_types = _safe_list("/passport-types")

    reference = {
        # Destination / origin are places, so these stay keyed by
        # country_name (what the /autocheck API and every other
        # country-picker in the app expects).
        "countries": (
            sorted(c["country_name"] for c in countries) if countries else FALLBACK_COUNTRIES
        ),
        # Nationality is a property of the traveller, not a place, so
        # it's presented using countries.nationality (e.g. "Indian",
        # "Saudi Arabian") rather than the country name. The API only
        # resolves nationality by country_name, so we still submit
        # country_name under the hood -- (label, value) pairs, same
        # pattern as purposes/passport_types below.
        "nationalities": (
            sorted(
                ((c["nationality"], c["country_name"]) for c in countries),
                key=lambda pair: pair[0],
            )
            if countries
            else [(name, name) for name in FALLBACK_COUNTRIES]
        ),
        "purposes": (
            [(p["purpose_code"], p["purpose_name"]) for p in purposes]
            if purposes
            else FALLBACK_PURPOSES
        ),
        "passport_types": (
            [(p["passport_code"], p["passport_name"]) for p in passport_types]
            if passport_types
            else FALLBACK_PASSPORT_TYPES
        ),
    }
    st.session_state["autocheck_reference"] = reference
    return reference


def _render_field_table(data, labels):
    if not data:
        st.caption("No rule configured for this category.")
        return

    rows = []
    for field, label in labels.items():
        if field not in data:
            continue
        value = data[field]
        if isinstance(value, bool):
            value = "Yes" if value else "No"
        elif value in (None, ""):
            value = "-"
        rows.append({"Requirement": label, "Value": value})

    st.table(rows)


def _render_decision(decision):
    status = decision.get("status", "")
    label, kind = STATUS_DISPLAY.get(status, (status, "info"))
    message = f"**{label}** — {decision.get('summary', '')}"

    if kind == "success":
        st.success(message)
    elif kind == "warning":
        st.warning(message)
    elif kind == "error":
        st.error(message)
    else:
        st.info(message)

    col1, col2, col3 = st.columns(3)
    groups = [
        (col1, "Requirements", decision.get("requirements", [])),
        (col2, "Warnings", decision.get("warnings", [])),
        (col3, "Blockers", decision.get("blockers", [])),
    ]
    for column, title, items in groups:
        with column:
            st.markdown(f"**{title}**")
            if items:
                for item in items:
                    st.markdown(f"- {item}")
            else:
                st.caption("None")


def _render_result(result):
    _render_decision(result["decision"])

    st.divider()

    tabs = st.tabs([label for label, _ in DOMAIN_TABS])
    for tab, (_, key) in zip(tabs, DOMAIN_TABS):
        with tab:
            data = result.get(key)
            _render_field_table(data, DOMAIN_LABELS[key])
            if key == "health" and data and data.get("vaccines"):
                st.markdown("**Vaccine requirements**")
                st.table(
                    [
                        {
                            "Vaccine": v["vaccine_name"],
                            "Certificate required": "Yes" if v["certificate_required"] else "No",
                        }
                        for v in data["vaccines"]
                    ]
                )

    st.divider()

    meta_col1, meta_col2 = st.columns(2)
    meta_col1.caption(f"Compliance check ID: {result['compliance_check_id']}")
    meta_col2.caption(f"Request ID: {result['request_id']}")

    with st.expander("View raw JSON"):
        st.json(result)


@_dialog("Auto Check Result")
def _show_result_dialog(result):
    _render_result(result)


def render_autocheck(client):
    st.title("Auto Check")
    st.caption(
        "Submit a traveller's details to evaluate visa, passport, transit, "
        "health, immigration, customs, and entry restriction requirements "
        "for their journey."
    )

    api_key = st.session_state.get("auth_client_api_key", DEFAULT_API_KEY)

    reference = _load_reference_data(client)

    nationality_labels = [label for label, _ in reference["nationalities"]]
    purpose_labels = [label for _, label in reference["purposes"]]
    passport_labels = [label for _, label in reference["passport_types"]]

    with st.form("autocheck_form"):
        col1, col2 = st.columns(2)

        with col1:
            # Nationality and "travelling from" are grouped together
            # here (rather than origin living in its own full-width
            # row) since origin only makes sense in relation to the
            # traveller's nationality.
            nationality_label = st.selectbox(
                "Nationality",
                nationality_labels,
                index=None,
                placeholder="Select nationality",
            )
            origin_choice = st.selectbox(
                "Travelling from (origin)",
                reference["countries"],
                index=None,
                placeholder="Not specified (any origin)",
                help=(
                    "Only needed if the traveller is departing from a country "
                    "other than their nationality, e.g. an Indian national "
                    "flying to Poland via Saudi Arabia. Leaving this blank "
                    "does NOT default to nationality -- it matches rules that "
                    "apply regardless of origin. Some health and entry-"
                    "restriction requirements depend on this."
                ),
            )

        with col2:
            destination = st.selectbox(
                "Destination",
                reference["countries"],
                index=None,
                placeholder="Select destination",
            )
            purpose_label = st.selectbox(
                "Purpose of travel",
                purpose_labels,
                index=None,
                placeholder="Select purpose of travel",
            )
            passport_label = st.selectbox(
                "Passport type",
                passport_labels,
                index=None,
                placeholder="Select passport type",
            )

        submitted = st.form_submit_button("Run auto-check", type="primary")

    if submitted:
        missing = [
            field_name
            for field_name, value in (
                ("Nationality", nationality_label),
                ("Destination", destination),
                ("Purpose of travel", purpose_label),
                ("Passport type", passport_label),
            )
            if value is None
        ]
        if missing:
            st.warning(f"Please fill in: {', '.join(missing)}.")
            return

        nationality = next(
            country_name
            for label, country_name in reference["nationalities"]
            if label == nationality_label
        )

        

        purpose_code = next(
            code for code, label in reference["purposes"] if label == purpose_label
        )
        passport_code = next(
            code for code, label in reference["passport_types"] if label == passport_label
        )

        payload = {
            "nationality": nationality,
            "destination": destination,
            "purpose": purpose_code,
            "passport_type": passport_code,
        }
        if origin_choice is not None:
            payload["origin"] = origin_choice

        try:
            with st.spinner("Running compliance check..."):
                result = client.create(
                    "/autocheck", payload, extra_headers={"X-API-Key": api_key}
                )
            st.session_state["autocheck_result"] = result
            _show_result_dialog(result)
        except APIError as e:
            st.error(f"API error {e.status_code}: {e.detail}")
            return
        except Exception as e:
            st.error(f"Request failed: {e}")
            return

    # A dialog only stays open for the run that triggered it -- any
    # later rerun (e.g. widget interaction elsewhere on the page)
    # closes it. This lets someone reopen their last result without
    # having to run the check again.
    result = st.session_state.get("autocheck_result")
    if result and st.button("View last result"):
        _show_result_dialog(result)