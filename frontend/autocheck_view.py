import streamlit as st
from datetime import date

from api_client import APIError

_dialog = getattr(st, "dialog", None) or st.experimental_dialog


def _dialog_factory(title):
   
    try:
        return _dialog(title, width="large")
    except TypeError:
        return _dialog(title)


_RESULT_DIALOG_DECORATOR = _dialog_factory("Auto Check Result")

#DEFAULT_API_KEY = "demo_api_key_123456789"

FALLBACK_COUNTRIES = [
    {"iso2": "IN", "country_name": "India", "nationality": "Indian"},
    {"iso2": "PL", "country_name": "Poland", "nationality": "Polish"},
    {"iso2": "SA", "country_name": "Saudi Arabia", "nationality": "Saudi Arabian"},
]
FALLBACK_AIRPORTS = [
    {"iata_code": "COK", "airport_name": "Cochin International Airport", "city": "Kochi"},
    {"iata_code": "DOH", "airport_name": "Hamad International Airport", "city": "Doha"},
    {"iata_code": "FRA", "airport_name": "Frankfurt Airport", "city": "Frankfurt"},
    {"iata_code": "DEL", "airport_name": "Indira Gandhi International Airport", "city": "Delhi"},
]
FALLBACK_PURPOSES = [
    ("TOUR", "Tourism"),
    ("BUSINESS", "Business"),
    ("STUDY", "Study"),
    ("WORK", "Employment"),
    ("MEDICAL", "Medical"),
]
FALLBACK_PASSPORT_TYPES = [("PP", "Ordinary Passport")]

PASSENGER_TYPES = ["ADULT", "CHILD", "INFANT", "CREW"]
SPECIAL_STATUSES = ["DIPLOMAT", "REFUGEE", "STATELESS", "SEAMAN", "MILITARY"]

STATUS_DISPLAY = {
    "CLEAR": ("Compliant", "success", "\u2713"),
    "ACTION_REQUIRED": ("Action Required", "warning", "!"),
    "NOT_PERMITTED": ("Entry Restricted", "error", "\u2715"),
    "CONDITIONAL": ("Conditional", "warning", "!"),
    "UNKNOWN": ("Unable To Determine", "info", "?"),
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

DOMAIN_ICONS = {
    "visa": "\U0001F6C2",           # passport control
    "passport": "\U0001F4D8",       # blue book
    "transit": "\u2708\uFE0F",      # airplane
    "health": "\U0001FA7A",         # stethoscope
    "immigration": "\U0001F6C3",    # customs
    "customs": "\U0001F4E6",        # package
    "entry_restriction": "\u26D4",  # no entry
}

# DOMAIN_TABS is a list of (label, key) pairs, e.g. ("Visa", "visa") --
# dict(DOMAIN_TABS) would key by label, not by key. This is the reverse
# lookup (key -> label) actually needed when going from a domain key back
# to its display label.
DOMAIN_LABELS_BY_KEY = {key: label for label, key in DOMAIN_TABS}


def _plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def _visa_sentences(d):
    s = []
    if d.get("visa_required"):
        s.append("A visa is required for this destination.")
        if d.get("visa_type"):
            s.append(f"The applicable visa category is {d['visa_type']}.")
        s.append(
            "The visa permits multiple entries."
            if d.get("multiple_entry")
            else "The visa permits a single entry only."
        )
    else:
        s.append("No visa is required for this destination.")
    if d.get("visa_on_arrival"):
        s.append("Visa on arrival is available to eligible travellers.")
    if d.get("evisa_available"):
        s.append("An e-Visa can be obtained online prior to departure.")
    if d.get("max_stay_days"):
        s.append(f"The maximum permitted stay is {_plural(d['max_stay_days'], 'day')} per visit.")
    if d.get("remarks"):
        s.append(d["remarks"])
    return s


def _passport_sentences(d):
    s = []
    if d.get("minimum_validity_months"):
        s.append(
            f"The passport must remain valid for at least "
            f"{_plural(d['minimum_validity_months'], 'month')} beyond the date of entry."
        )
    if d.get("blank_pages_required"):
        s.append(f"The passport must contain at least {_plural(d['blank_pages_required'], 'blank page')}.")
    if d.get("machine_readable_required"):
        s.append("The passport must be machine-readable.")
    s.append(
        "Damaged passports are accepted."
        if d.get("damaged_passport_allowed")
        else "Damaged passports are not accepted."
    )
    s.append(
        "Temporary or emergency passports are accepted."
        if d.get("temporary_passport_allowed")
        else "Temporary or emergency passports are not accepted."
    )
    if d.get("passport_issue_date_required"):
        s.append("The passport's date of issue must be verifiable.")
    if d.get("remarks"):
        s.append(d["remarks"])
    return s


def _transit_sentences(d):
    s = []
    s.append(
        "A transit visa is required."
        if d.get("transit_visa_required")
        else "No transit visa is required."
    )
    s.append(
        "Airside transit is permitted without clearing immigration."
        if d.get("airside_transit_allowed")
        else "Airside transit is not permitted; travellers must clear immigration."
    )
    if d.get("baggage_collection_required"):
        s.append("Baggage must be collected and re-checked during transit.")
    s.append(
        "Overnight transit is permitted."
        if d.get("overnight_transit_allowed")
        else "Overnight transit is not permitted."
    )
    if d.get("max_transit_hours"):
        s.append(f"The maximum permitted transit time is {_plural(d['max_transit_hours'], 'hour')}.")
    if d.get("remarks"):
        s.append(d["remarks"])
    return s


def _health_sentences(d):
    s = []
    s.append(
        "A health declaration form must be completed."
        if d.get("health_form_required")
        else "No health declaration form is required."
    )
    if d.get("quarantine_required"):
        if d.get("quarantine_days"):
            s.append(f"Quarantine of {_plural(d['quarantine_days'], 'day')} is required on arrival.")
        else:
            s.append("Quarantine is required on arrival.")
    else:
        s.append("No quarantine is required on arrival.")
    s.append(
        "A medical certificate must be presented on arrival."
        if d.get("medical_certificate_required")
        else "No medical certificate is required on arrival."
    )
    for v in d.get("vaccines", []) or []:
        name = v.get("vaccine_name", "the required vaccine")
        if v.get("certificate_required"):
            s.append(f"A valid {name} vaccination certificate must be carried.")
        else:
            s.append(f"{name} vaccination is recommended, though no certificate is required.")
    if d.get("remarks"):
        s.append(d["remarks"])
    return s


def _immigration_sentences(d):
    s = []
    s.append(
        "Proof of onward or return travel must be carried."
        if d.get("onward_ticket_required")
        else "No proof of onward or return travel is required."
    )
    s.append(
        "Proof of accommodation must be carried."
        if d.get("accommodation_proof_required")
        else "No proof of accommodation is required."
    )
    s.append(
        "Proof of sufficient funds must be carried."
        if d.get("proof_of_funds_required")
        else "No proof of sufficient funds is required."
    )
    if d.get("biometric_required"):
        s.append("Biometric verification (fingerprints and/or photo) is required on arrival.")
    if d.get("interview_required"):
        s.append("An immigration interview may be required on arrival.")
    if d.get("arrival_card_required"):
        if d.get("digital_arrival_card"):
            s.append("An arrival card must be completed and can be submitted digitally.")
        else:
            s.append("A physical arrival card must be completed.")
    if d.get("arrival_registration_required"):
        s.append("Registration with local authorities is required after arrival.")
    if d.get("remarks"):
        s.append(d["remarks"])
    return s


def _customs_sentences(d):
    s = []
    if d.get("alcohol_limit"):
        s.append(f"The permitted alcohol allowance is {d['alcohol_limit']}.")
    if d.get("tobacco_limit"):
        s.append(f"The permitted tobacco allowance is {d['tobacco_limit']}.")
    currency = d.get("currency")
    if d.get("currency_limit_amount"):
        amount_str = f"{currency} {d['currency_limit_amount']}" if currency else str(d["currency_limit_amount"])
        s.append(f"Amounts of {amount_str} or more must be declared on arrival.")
    elif d.get("currency_declaration_required"):
        s.append("Currency must be declared on arrival.")
    if d.get("medication_rules"):
        s.append(f"Medication rules: {d['medication_rules']}")
    if d.get("prohibited_items"):
        s.append(f"The following items are prohibited: {d['prohibited_items']}.")
    if d.get("restricted_items"):
        s.append(f"The following items are restricted: {d['restricted_items']}.")
    if d.get("pet_import_rules"):
        s.append(f"Verify pet import requirements before travelling: {d['pet_import_rules']}")
    if d.get("remarks"):
        s.append(d["remarks"])
    return s


def _entry_restriction_sentences(d):
    s = []
    if d.get("restriction_type"):
        s.append(f"A {d['restriction_type']} entry restriction applies to this journey.")
    if d.get("reason"):
        s.append(f"Reason: {d['reason']}")
    if d.get("effective_date"):
        s.append(f"This restriction has been in effect since {d['effective_date']}.")
    if d.get("expiry_date"):
        s.append(f"This restriction is scheduled to expire on {d['expiry_date']}.")
    if d.get("source"):
        s.append(f"Source: {d['source']}")
    if d.get("remarks"):
        s.append(d["remarks"])
    return s


DOMAIN_SENTENCE_BUILDERS = {
    "visa": _visa_sentences,
    "passport": _passport_sentences,
    "transit": _transit_sentences,
    "health": _health_sentences,
    "immigration": _immigration_sentences,
    "customs": _customs_sentences,
    "entry_restriction": _entry_restriction_sentences,
}


def _load_reference_data(client):
    if "autocheck_reference" in st.session_state:
        return st.session_state["autocheck_reference"]

    def _safe_list(path):
        try:
            return client.list(path)
        except (APIError, Exception):
            return None

    countries = _safe_list("/countries")
    airports = _safe_list("/airports")
    purposes = _safe_list("/purposes")
    passport_types = _safe_list("/passport-types")

    if not countries:
        countries = FALLBACK_COUNTRIES
    if not airports:
        airports = FALLBACK_AIRPORTS

    reference = {
        # /autocheck now resolves nationality/passport issuing_country/
        # country_of_residence by ISO 3166-1 alpha-2 code, not by full
        # country name -- these are (label, iso2) pairs so the UI can
        # still show a human-readable name while submitting the code
        # the API actually expects.
        "countries": sorted(
            ((c["country_name"], c["iso2"]) for c in countries),
            key=lambda pair: pair[0],
        ),
        # Nationality is a property of the traveller, not a place, so
        # it's presented using countries.nationality (e.g. "Indian",
        # "Saudi Arabian") -- the value submitted is still the
        # country's iso2 code, same as issuing_country.
        "nationalities": sorted(
            ((c["nationality"], c["iso2"]) for c in countries),
            key=lambda pair: pair[0],
        ),
        # journey.origin/destination and transit_points.airport are now
        # IATA airport codes, not country names -- airports without an
        # iata_code (rail/sea ports etc., if any exist in the data)
        # can't be selected here since /autocheck can't resolve them.
        "airports": sorted(
            (
                (f"{a['airport_name']} ({a['iata_code']}) \u2014 {a.get('city', '')}", a["iata_code"])
                for a in airports
                if a.get("iata_code")
            ),
            key=lambda pair: pair[0],
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


_REPORT_CSS = """
<style>
.tac-report {
    font-family: "Source Sans Pro", "Segoe UI", Arial, sans-serif;
    /* Fixed, theme-independent palette: this card renders the same
       whether the surrounding Streamlit app is in light or dark mode.
       Earlier styling used translucent overlays tuned for a dark host
       background, which turned into low-contrast light-grey-on-white
       text under a light theme. Solid colors here avoid that. */
    background: #ffffff;
    color: #1b2430;
    border-radius: 10px;
    padding: 4px 2px;
}
.tac-banner {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 18px 22px;
    border-radius: 8px;
    margin-bottom: 18px;
    border: 1px solid;
}
.tac-banner.tac-success { background: #eafaf1; border-color: #2fa968; }
.tac-banner.tac-warning { background: #fdf3e2; border-color: #d18f1f; }
.tac-banner.tac-error   { background: #fdecea; border-color: #d1483f; }
.tac-banner-icon {
    flex: 0 0 auto;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 17px;
    color: #fff;
}
.tac-success .tac-banner-icon { background: #1f9e5c; }
.tac-warning .tac-banner-icon { background: #c07f14; }
.tac-error   .tac-banner-icon { background: #c73e35; }
.tac-banner-text .tac-banner-title {
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    margin-bottom: 3px;
}
.tac-success .tac-banner-title { color: #157a45; }
.tac-warning .tac-banner-title { color: #9c6510; }
.tac-error   .tac-banner-title { color: #a5322a; }
.tac-banner-summary {
    font-size: 14.5px;
    color: #2b3442;
    line-height: 1.45;
}
.tac-meta-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 10px 28px;
    padding: 12px 4px 18px 4px;
    border-bottom: 1px solid #e3e6eb;
    margin-bottom: 18px;
}
.tac-meta-item { font-size: 13px; color: #5b6472; }
.tac-meta-item b { color: #1b2430; font-weight: 600; }
.tac-section-title {
    font-size: 12.5px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #5b6472;
    margin: 4px 0 10px 0;
}
.tac-card {
    background: #f7f8fa;
    border: 1px solid #e3e6eb;
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 14px;
}
.tac-list { list-style: none; margin: 0; padding: 0; }
.tac-list li {
    position: relative;
    padding-left: 20px;
    margin-bottom: 8px;
    font-size: 14px;
    line-height: 1.5;
    color: #262e3a;
}
.tac-list.tac-req li::before { content: "\\2713"; position: absolute; left: 0; color: #1f9e5c; font-weight: 700; }
.tac-list.tac-warn li::before { content: "\\26A0"; position: absolute; left: 0; color: #c07f14; font-size: 12px; top: 1px; }
.tac-list.tac-block li::before { content: "\\2715"; position: absolute; left: 0; color: #c73e35; font-weight: 700; }
.tac-list.tac-plain li::before { content: "\\2022"; position: absolute; left: 0; color: #8b93a1; }
.tac-empty { font-size: 13.5px; color: #7c8494; font-style: italic; }
.tac-footer {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 6px;
    padding-top: 14px;
    border-top: 1px solid #e3e6eb;
}
.tac-tag {
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 12px;
    color: #5b6472;
    background: #f0f1f4;
    border: 1px solid #dfe2e8;
    border-radius: 5px;
    padding: 3px 9px;
}
</style>
"""


def _sentence_list(items, variant):
    if not items:
        return '<p class="tac-empty">None identified.</p>'
    lis = "".join(f"<li>{item}</li>" for item in items)
    return f'<ul class="tac-list tac-{variant}">{lis}</ul>'


def _render_decision(decision):
    status = decision.get("status", "")
    label, kind, icon = STATUS_DISPLAY.get(status, (status, "info", "\u2022"))
    variant = {"success": "tac-success", "warning": "tac-warning", "error": "tac-error"}.get(kind, "tac-success")

    st.markdown(
        f"""
        <div class="tac-banner {variant}">
            <div class="tac-banner-icon">{icon}</div>
            <div class="tac-banner-text">
                <div class="tac-banner-title">{label}</div>
                <div class="tac-banner-summary">{decision.get('summary', '')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    groups = [
        (col1, "Requirements", decision.get("requirements", []), "req"),
        (col2, "Warnings", decision.get("warnings", []), "warn"),
        (col3, "Blockers", decision.get("blockers", []), "block"),
    ]
    for column, title, items, variant_key in groups:
        with column:
            st.markdown(
                f'<div class="tac-section-title">{title}</div>'
                f'<div class="tac-card">{_sentence_list(items, variant_key)}</div>',
                unsafe_allow_html=True,
            )


def _render_domain(key, data):
    if not data:
        st.markdown(
            '<div class="tac-card"><p class="tac-empty">No rule is configured for this category on '
            "this route — nothing further to report.</p></div>",
            unsafe_allow_html=True,
        )
        return
    builder = DOMAIN_SENTENCE_BUILDERS[key]
    sentences = builder(data)
    st.markdown(
        f'<div class="tac-card">{_sentence_list(sentences, "plain")}</div>',
        unsafe_allow_html=True,
    )


def _render_domain_grid(result):
 
    st.markdown('<div class="tac-section-title" style="margin-top:20px;">Requirement Detail</div>', unsafe_allow_html=True)
    st.markdown('<p class="tac-empty" style="margin-bottom:10px;">Select a category to view its full requirements.</p>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (label, key) in enumerate(DOMAIN_TABS):
        with cols[i % 4]:
            has_data = bool(result.get(key))
            icon = DOMAIN_ICONS.get(key, "\u2022")
            button_label = f"{icon}  {label}" if has_data else f"{icon}  {label} —"
            if st.button(button_label, key=f"tac_domain_btn_{key}", use_container_width=True):
                st.session_state["autocheck_active_domain"] = key
                st.rerun()

    close_col, _spacer = st.columns([1, 3])
    with close_col:
        if st.button("Close", key="tac_close_dialog", use_container_width=True):
            st.session_state["autocheck_dialog_open"] = False
            st.session_state["autocheck_active_domain"] = None
            st.rerun()


def _render_domain_detail(result, key):
    label = DOMAIN_LABELS_BY_KEY[key]
    if st.button("\u2190 Back to summary", key="tac_domain_back"):
        st.session_state["autocheck_active_domain"] = None
        st.rerun()

    st.markdown(
        f'<div class="tac-section-title" style="margin-top:14px;">{DOMAIN_ICONS.get(key, "")}  {label} Requirements</div>',
        unsafe_allow_html=True,
    )
    _render_domain(key, result.get(key))


def _render_result(result, form_context=None):
    st.markdown(_REPORT_CSS, unsafe_allow_html=True)
    st.markdown('<div class="tac-report">', unsafe_allow_html=True)

    active_domain = st.session_state.get("autocheck_active_domain")

    if active_domain:
        _render_domain_detail(result, active_domain)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if form_context:
        items = "".join(
            f'<div class="tac-meta-item"><b>{v}</b><br/>{k}</div>' for k, v in form_context
        )
        st.markdown(f'<div class="tac-meta-strip">{items}</div>', unsafe_allow_html=True)

    _render_decision(result["decision"])

    _render_domain_grid(result)

    st.markdown(
        f"""
        <div class="tac-footer">
            <span class="tac-tag">Compliance check ID: {result['compliance_check_id']}</span>
            <span class="tac-tag">Request ID: {result['request_id']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("View raw JSON"):
        st.json(result)


@_RESULT_DIALOG_DECORATOR
def _show_result_dialog(result, form_context=None):
    _render_result(result, form_context)


def render_autocheck(client):
    st.title("Auto Check")
    st.caption(
        "Submit a traveller's details to evaluate visa, passport, transit, "
        "health, immigration, customs, and entry restriction requirements "
        "for their journey."
    )

    api_key = st.session_state.get("auth_client_api_key")
    if not api_key:
        st.error("No API key found in session. Please log in again.")
        st.stop()

    reference = _load_reference_data(client)

    nationality_labels = [label for label, _ in reference["nationalities"]]
    country_labels = [label for label, _ in reference["countries"]]
    airport_labels = [label for label, _ in reference["airports"]]
    purpose_labels = [label for _, label in reference["purposes"]]
    passport_labels = [label for _, label in reference["passport_types"]]

    with st.form("autocheck_form"):
        st.markdown("**Traveller**")
        col1, col2 = st.columns(2)

        with col1:
            nationality_label = st.selectbox(
                "Nationality",
                nationality_labels,
                index=None,
                placeholder="Select nationality",
            )
            passenger_type = st.selectbox(
                "Passenger type",
                PASSENGER_TYPES,
                index=0,
            )

        with col2:
            residence_label = st.selectbox(
                "Country of residence",
                country_labels,
                index=None,
                placeholder="Same as nationality",
                help="Only needed if different from nationality.",
            )
            special_status = st.selectbox(
                "Special status",
                ["(none)"] + SPECIAL_STATUSES,
                index=0,
                help="Diplomatic, refugee, seaman, or military status can change which rules apply.",
            )

        st.markdown("**Passport**")
        col3, col4, col5 = st.columns(3)

        with col3:
            passport_issuing_label = st.selectbox(
                "Issuing country",
                country_labels,
                index=None,
                placeholder="Same as nationality",
                help="Leave blank if the passport was issued by the nationality country.",
            )
        with col4:
            passport_label = st.selectbox(
                "Passport type",
                passport_labels,
                index=None,
                placeholder="Select passport type",
            )
        with col5:
            passport_valid_until = st.date_input(
                "Passport valid until",
                value=None,
                min_value=date.today(),
            )

        st.markdown("**Journey**")
        col6, col7 = st.columns(2)

        with col6:
            origin_label = st.selectbox(
                "Departing from (airport)",
                airport_labels,
                index=None,
                placeholder="Select origin airport",
            )
            travel_date = st.date_input(
                "Travel date",
                value=None,
                min_value=date.today(),
            )

        with col7:
            destination_label = st.selectbox(
                "Arriving at (airport)",
                airport_labels,
                index=None,
                placeholder="Select destination airport",
            )
            purpose_label = st.selectbox(
                "Purpose of travel",
                purpose_labels,
                index=None,
                placeholder="Select purpose of travel",
            )

        return_date = st.date_input(
            "Return date (optional)",
            value=None,
            min_value=date.today(),
        )

        with st.expander("Add a transit stop (optional)"):
            transit_label = st.selectbox(
                "Transit airport",
                airport_labels,
                index=None,
                placeholder="No transit stop",
                key="autocheck_transit_airport",
            )
            tcol1, tcol2 = st.columns(2)
            with tcol1:
                transit_duration = st.number_input(
                    "Layover duration (minutes)",
                    min_value=0,
                    value=90,
                    step=15,
                )
                transit_requires_immigration = st.checkbox(
                    "Requires clearing immigration at this stop",
                    value=False,
                )
            with tcol2:
                transit_separate_ticket = st.checkbox(
                    "Booked on a separate ticket",
                    value=False,
                )

        submitted = st.form_submit_button("Run auto-check", type="primary")

    if submitted:
        missing = [
            field_name
            for field_name, value in (
                ("Nationality", nationality_label),
                ("Passport type", passport_label),
                ("Passport valid-until date", passport_valid_until),
                ("Origin airport", origin_label),
                ("Destination airport", destination_label),
                ("Travel date", travel_date),
                ("Purpose of travel", purpose_label),
            )
            if value is None
        ]
        if missing:
            st.warning(f"Please fill in: {', '.join(missing)}.")
            return

        nationality_iso2 = next(
            iso2 for label, iso2 in reference["nationalities"] if label == nationality_label
        )
        origin_iata = next(
            iata for label, iata in reference["airports"] if label == origin_label
        )
        destination_iata = next(
            iata for label, iata in reference["airports"] if label == destination_label
        )
        purpose_code = next(
            code for code, label in reference["purposes"] if label == purpose_label
        )
        passport_code = next(
            code for code, label in reference["passport_types"] if label == passport_label
        )

        passport_payload = {
            "type": passport_code,
            "valid_until": passport_valid_until.isoformat(),
        }
        if passport_issuing_label is not None:
            passport_payload["issuing_country"] = next(
                iso2 for label, iso2 in reference["countries"] if label == passport_issuing_label
            )

        passenger_payload = {
            "nationality": nationality_iso2,
            "passport": passport_payload,
            "passenger_type": passenger_type,
        }
        if residence_label is not None:
            passenger_payload["country_of_residence"] = next(
                iso2 for label, iso2 in reference["countries"] if label == residence_label
            )
        if special_status != "(none)":
            passenger_payload["special_status"] = special_status

        journey_payload = {
            "origin": origin_iata,
            "destination": destination_iata,
            "travel_date": travel_date.isoformat(),
            "purpose": purpose_code,
        }
        if return_date is not None:
            journey_payload["return_date"] = return_date.isoformat()

        if transit_label is not None:
            transit_iata = next(
                iata for label, iata in reference["airports"] if label == transit_label
            )
            journey_payload["transit_points"] = [
                {
                    "airport": transit_iata,
                    "duration_minutes": int(transit_duration),
                    "requires_immigration": transit_requires_immigration,
                    "separate_ticket": transit_separate_ticket,
                }
            ]

        payload = {
            "passenger": passenger_payload,
            "journey": journey_payload,
        }

        form_context = [
            ("Nationality", nationality_label),
            ("Origin", origin_label),
            ("Destination", destination_label),
            ("Travel date", travel_date.isoformat()),
            ("Purpose of travel", purpose_label),
            ("Passport type", passport_label),
        ]
        if transit_label is not None:
            form_context.append(("Transit via", transit_label))

        try:
            with st.spinner("Running compliance check..."):
                result = client.create(
                    "/autocheck", payload, extra_headers={"X-API-Key": api_key}
                )
            st.session_state["autocheck_result"] = result
            st.session_state["autocheck_form_context"] = form_context
            st.session_state["autocheck_active_domain"] = None
            st.session_state["autocheck_dialog_open"] = True
        except APIError as e:
            st.error(f"API error {e.status_code}: {e.detail}")
            return
        except Exception as e:
            st.error(f"Request failed: {e}")
            return


    result = st.session_state.get("autocheck_result")
    if result and st.button("View last result"):
        st.session_state["autocheck_active_domain"] = None
        st.session_state["autocheck_dialog_open"] = True

    if st.session_state.get("autocheck_dialog_open") and result:
        _show_result_dialog(result, st.session_state.get("autocheck_form_context"))