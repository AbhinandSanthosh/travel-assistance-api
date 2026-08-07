"""
Auto Check view: submits a traveller's details to POST /autocheck and
renders the compliance decision plus the full per-category travel
requirement breakdown. Uses the same APIClient/APIError conventions as
the rest of the console.
"""

import streamlit as st

from api_client import APIError

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
        "countries": (
            sorted(c["country_name"] for c in countries) if countries else FALLBACK_COUNTRIES
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


def render_autocheck(client):
    st.title("Auto Check")
    st.caption(
        "Submit a traveller's details to evaluate visa, passport, transit, "
        "health, immigration, customs, and entry restriction requirements "
        "for their journey."
    )

    reference = _load_reference_data(client)

    with st.form("autocheck_form"):
        col1, col2 = st.columns(2)

        with col1:
            nationality = st.selectbox("Nationality", reference["countries"])
            purpose_label = st.selectbox(
                "Purpose of travel",
                [label for _, label in reference["purposes"]],
            )

        with col2:
            destination = st.selectbox(
                "Destination",
                reference["countries"],
                index=min(1, len(reference["countries"]) - 1),
            )
            passport_label = st.selectbox(
                "Passport type",
                [label for _, label in reference["passport_types"]],
            )

        api_key = st.text_input(
            "API key",
            value=st.session_state.get("autocheck_api_key", DEFAULT_API_KEY),
            type="password",
        )

        submitted = st.form_submit_button("Run auto-check", type="primary")

    if submitted:
        if nationality == destination:
            st.warning("Nationality and destination must be different countries.")
            return

        purpose_code = next(
            code for code, label in reference["purposes"] if label == purpose_label
        )
        passport_code = next(
            code for code, label in reference["passport_types"] if label == passport_label
        )

        payload = {
            "api_key": api_key,
            "nationality": nationality,
            "destination": destination,
            "purpose": purpose_code,
            "passport_type": passport_code,
        }

        try:
            with st.spinner("Running compliance check..."):
                result = client.create("/autocheck", payload)
            st.session_state["autocheck_result"] = result
            st.session_state["autocheck_api_key"] = api_key
        except APIError as e:
            st.error(f"API error {e.status_code}: {e.detail}")
            return
        except Exception as e:
            st.error(f"Request failed: {e}")
            return

    result = st.session_state.get("autocheck_result")
    if result:
        _render_result(result)