import json
from datetime import date, datetime

import pandas as pd
import streamlit as st

from api_client import APIClient, APIError
from entities import ENTITIES, ENUMS, CATEGORY_ORDER
from auth_gate import render_gate, render_sidebar_identity
import autocheck_view

RELATIONS = {
    # Reference
    "region_id": {
        "endpoint": "/regions",
        "label_field": "region_name",
    },
    "currency_id": {
        "endpoint": "/currencies",
        "label_field": "currency_name",
    },
    "country_id": {
        "endpoint": "/countries",
        "label_field": "country_name",
    },
    "destination_country_id": {
        "endpoint": "/countries",
        "label_field": "country_name",
    },
    "nationality_country_id": {
        "endpoint": "/countries",
        "label_field": "country_name",
    },
    "transit_country_id": {
        "endpoint": "/countries",
        "label_field": "country_name",
    },
    "passport_type_id": {
        "endpoint": "/passport-types",
        "label_field": "passport_name",
    },
    "visa_type_id": {
        "endpoint": "/visa-types",
        "label_field": "visa_name",
    },
    "purpose_id": {
        "endpoint": "/purposes",
        "label_field": "purpose_name",
    },
    "authorization_id": {
        "endpoint": "/travel-authorizations/",
        "label_field": "authorization_name",
    },
    "transit_airport_id": {
        "endpoint": "/airports",
        "label_field": "airport_name",
    },
    "vaccine_id": {
        "endpoint": "/vaccines",
        "label_field": "vaccine_name",
    },

    # Administration
    "role_id": {
        "endpoint": "/roles",
        "label_field": "role_name",
    },
    "permission_id": {
        "endpoint": "/permissions",
        "label_field": "permission_name",
    },
    "client_id": {
        "endpoint": "/api-clients",
        "label_field": "client_name",
    },

    # Rule Management
    "status_id": {
        "endpoint": "/rule-statuses",
        "label_field": "status_name",
    },
    "rule_id": {
        "endpoint": "/rules",
        "label_field": "rule_code",
    },
    "health_rule_id": {
        "endpoint": "/health-rules",
        "label_field": "remarks",
    },
    "new_version_id": {
        "endpoint": "/rule-versions",
        "label_field": "version_number",
    },
    "previous_version_id": {
        "endpoint": "/rule-versions",
        "label_field": "version_number",
    },

    "source_id": {
        "endpoint": "/source-registries",
        "label_field": "authority_name",
    },
    "document_id": {
        "endpoint": "/source-documents",
        "label_field": "document_name",
    },

    
    "reviewer_id": {
        "endpoint": "/users",
        "label_field": "full_name",
    },
    "validator_id": {
        "endpoint": "/users",
        "label_field": "full_name",
    },
    "user_id": {
        "endpoint": "/users",
        "label_field": "full_name",
    },
}


def _relation_records(field_name):
   
    relation = RELATIONS.get(field_name)
    if not relation:
        return []

    cache_key = f"relation_options__{field_name}"

    
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    try:
        records = client.list(relation["endpoint"]) or []
        st.session_state[cache_key] = records
        return records
    except APIError as e:
        st.error(
            f"Could not load options for '{field_name}': "
            f"API error {e.status_code}: {e.detail}"
        )
        return []
    except Exception as e:
        st.error(
            f"Could not load options for '{field_name}': {e}"
        )
        return []


def _relation_options(field_name, current_value=None, required=True):
   
    relation = RELATIONS[field_name]
    label_field = relation["label_field"]
    records = _relation_records(field_name)

    display_to_id = {}
    current_id = None

    if current_value is not None and current_value != "":
        try:
            current_id = int(current_value)
        except (TypeError, ValueError):
            current_id = current_value

    for record in records:
        if not isinstance(record, dict):
            continue

        record_id = record.get("id")

       
        if record_id is None:
            for possible_id in (
                "region_id",
                "currency_id",
                "country_id",
                "passport_type_id",
                "visa_type_id",
                "purpose_id",
                "authorization_id",
                "airport_id",
                "vaccine_id",
                "role_id",
                "permission_id",
                "client_id",
                "status_id",
                "rule_id",
                "health_rule_id",
                "version_id",
                "source_id",
                "document_id",
                "user_id",
            ):
                if record.get(possible_id) is not None:
                    record_id = record[possible_id]
                    break

        if record_id is None:
            continue

        display_name = record.get(label_field)

        if display_name is None:
            display_name = record.get("name", record_id)

        display_text = f"{record_id} - {display_name}"

        if display_text not in display_to_id:
            display_to_id[display_text] = record_id

    display_options = list(display_to_id.keys())

    if not required:
        display_options = ["(none)"] + display_options

    selected_index = 0

    if current_id is not None:
        for index, display_text in enumerate(display_options):
            if display_to_id.get(display_text) == current_id:
                selected_index = index
                break

    return display_options, display_to_id, selected_index


def _render_relation_field(field, key, current_value=None, required=True, help_text=None):
    """
    Render a foreign-key field as a dropdown while returning the actual ID.
    """
    name = field["name"]
    label = name.replace("_id", "").replace("_", " ").title()
    label += " *" if required else ""

    options, display_to_id, selected_index = _relation_options(
        name,
        current_value=current_value,
        required=required,
    )

    if not options:
        st.warning(f"No records available for {label}.")
        return None

    choice = st.selectbox(
        label,
        options=options,
        index=selected_index,
        help=help_text,
        key=key,
    )

    if choice == "(none)":
        return None

    return display_to_id.get(choice)

st.set_page_config(page_title="Travel Assistance API Console", page_icon="🧳", layout="wide")


if "base_url" not in st.session_state:
    st.session_state.base_url = "http://localhost:8000"

with st.sidebar:
    st.title("🧳 Travel Assistance API")
    st.session_state.base_url = st.text_input("API base URL", value=st.session_state.base_url)

    if st.button("🔌 Test connection", use_container_width=True):
        try:
            health = APIClient(st.session_state.base_url).health()
            st.success(f"Connected — {health}")
        except Exception as e:
            st.error(f"Could not reach API: {e}")


client = render_gate(st.session_state.base_url)
if client is None:
    st.stop()

render_sidebar_identity(st.session_state.base_url)


if st.session_state.get("auth_role") == "client":
    autocheck_view.render_autocheck(client)
    st.stop()


with st.sidebar:
    st.divider()
    st.caption("ENTITY")

    if st.button("🔄 Refresh reference options", use_container_width=True):
        for _key in list(st.session_state.keys()):
            if _key.startswith("relation_options__"):
                st.session_state.pop(_key, None)

    category = st.selectbox("Category", CATEGORY_ORDER)
    names_in_category = [n for n, meta in ENTITIES.items() if meta["category"] == category]
    entity_name = st.radio("Entity", sorted(names_in_category), label_visibility="collapsed")

entity = ENTITIES[entity_name]
ops = entity["ops"]
endpoint = entity["endpoint"]

st.title(entity_name)
st.caption(f"`{endpoint}`  ·  supports: {', '.join(sorted(ops))}")


# --------------------------------------------------------------------------
# Field rendering helpers
# --------------------------------------------------------------------------
def _widget_key(prefix, name):
    return f"{prefix}__{entity_name}__{name}"


def render_field(field, key_prefix, current_value=None, force_optional=False):
    """Render a single input widget for a field and return the python value entered."""
    name = field["name"]
    ftype = field["type"]
    required = field["required"] and not force_optional
    label = name.replace("_", " ").title() + (" *" if required else "")
    help_text = field.get("help")
    key = _widget_key(key_prefix, name)

    if ftype == "str":
        return st.text_input(label, value=current_value or "", help=help_text, key=key) or None

    if ftype == "text":
        return st.text_area(label, value=current_value or "", help=help_text, key=key) or None

    if ftype == "email":
        return st.text_input(label, value=current_value or "", help=help_text or "user@example.com", key=key) or None

    
    if ftype == "int" and name in RELATIONS:
        return _render_relation_field(
            field=field,
            key=key,
            current_value=current_value,
            required=required,
            help_text=help_text,
        )

    if ftype == "int":
        default_val = field.get("default")
        val = st.text_input(
            label,
            value="" if current_value is None else str(current_value),
            help=help_text or ("integer" if default_val is None else f"integer, default {default_val}"),
            key=key,
        )
        if val == "":
            return None
        try:
            return int(val)
        except ValueError:
            st.warning(f"'{name}' must be an integer")
            return None

    if ftype == "decimal":
        val = st.text_input(
            label,
            value="" if current_value is None else str(current_value),
            help=help_text or "decimal number",
            key=key,
        )
        if val == "":
            return None
        try:
            return float(val)
        except ValueError:
            st.warning(f"'{name}' must be a number")
            return None

    if ftype == "bool":
        default_val = field.get("default", False)
        base = current_value if current_value is not None else default_val
        return st.checkbox(label, value=bool(base), help=help_text, key=key)

    if ftype == "date":
        if isinstance(current_value, str) and current_value:
            try:
                current_value = date.fromisoformat(current_value[:10])
            except ValueError:
                current_value = None
        use_date = st.checkbox(f"Set {label}", value=current_value is not None, key=key + "__toggle") \
            if not required else True
        if not use_date:
            return None
        d = st.date_input(label, value=current_value or date.today(), help=help_text, key=key)
        return d.isoformat()

    if ftype == "datetime":
        if isinstance(current_value, str) and current_value:
            try:
                current_value = datetime.fromisoformat(current_value.replace("Z", "+00:00"))
            except ValueError:
                current_value = None
        use_dt = st.checkbox(f"Set {label}", value=current_value is not None, key=key + "__toggle") \
            if not required else True
        if not use_dt:
            return None
        col1, col2 = st.columns(2)
        d = col1.date_input(label, value=(current_value or datetime.now()).date(), key=key + "__d")
        t = col2.time_input("Time", value=(current_value or datetime.now()).time(), key=key + "__t")
        return datetime.combine(d, t).isoformat()

    if ftype == "enum":
        options = ENUMS[field["enum"]]
        idx = options.index(current_value) if current_value in options else 0
        if not required:
            options_with_blank = ["(none)"] + options
            idx = options_with_blank.index(current_value) if current_value in options_with_blank else 0
            choice = st.selectbox(label, options_with_blank, index=idx, help=help_text, key=key)
            return None if choice == "(none)" else choice
        choice = st.selectbox(label, options, index=idx, help=help_text, key=key)
        return choice

    if ftype == "json":
        default_text = json.dumps(current_value, indent=2) if current_value is not None else ""
        text = st.text_area(label + " (JSON)", value=default_text, help=help_text or "Valid JSON object/array", key=key)
        if not text.strip():
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            st.warning(f"'{name}' is not valid JSON: {e}")
            return "__INVALID__"

    st.text_input(label, key=key)
    return None


def render_form_fields(fields, key_prefix, record=None, force_optional=False):
    """Render a list of fields two-per-row where practical; return {name: value}."""
    values = {}
    simple_types = {"str", "int", "decimal", "bool", "email"}
    i = 0
    while i < len(fields):
        field = fields[i]
        if field["type"] in simple_types and i + 1 < len(fields) and fields[i + 1]["type"] in simple_types:
            c1, c2 = st.columns(2)
            with c1:
                values[field["name"]] = render_field(
                    field, key_prefix, (record or {}).get(field["name"]), force_optional
                )
            nxt = fields[i + 1]
            with c2:
                values[nxt["name"]] = render_field(
                    nxt, key_prefix, (record or {}).get(nxt["name"]), force_optional
                )
            i += 2
        else:
            values[field["name"]] = render_field(
                field, key_prefix, (record or {}).get(field["name"]), force_optional
            )
            i += 1
    return values


def clean_payload(values, drop_none=True):
    invalid = [k for k, v in values.items() if v == "__INVALID__"]
    if invalid:
        return None, invalid
    if drop_none:
        return {k: v for k, v in values.items() if v is not None}, []
    return values, []


def flatten_for_table(records):
    """Turn list of (possibly nested) API records into a flat DataFrame."""
    if not records:
        return pd.DataFrame()
    flat = []
    for r in records:
        row = {}
        for k, v in r.items():
            if isinstance(v, dict):
                display = v.get("country_name") or v.get("region_name") or v.get("currency_name") or v.get("id")
                row[k] = display
            elif isinstance(v, list):
                row[k] = f"[{len(v)} items]"
            else:
                row[k] = v
        flat.append(row)
    return pd.DataFrame(flat)


# --------------------------------------------------------------------------
# Tabs: Browse / Create / Update / Delete
# --------------------------------------------------------------------------
tab_labels = ["📋 Browse"]
if "create" in ops:
    tab_labels.append("➕ Create")
if "update" in ops:
    tab_labels.append("✏️ Update")
if "delete" in ops:
    tab_labels.append("🗑️ Delete")

tabs = st.tabs(tab_labels)
tab_map = dict(zip(tab_labels, tabs))

# ---------------- Browse ----------------
with tab_map["📋 Browse"]:
    if st.button("🔄 Refresh list", key=f"refresh__{entity_name}"):
        st.session_state.pop(f"list_cache__{entity_name}", None)

    cache_key = f"list_cache__{entity_name}"
    if cache_key not in st.session_state:
        try:
            st.session_state[cache_key] = client.list(endpoint) or []
        except APIError as e:
            st.error(f"API error {e.status_code}: {e.detail}")
            st.session_state[cache_key] = []
        except Exception as e:
            st.error(f"Could not reach API at {st.session_state.base_url}. {e}")
            st.session_state[cache_key] = []

    records = st.session_state[cache_key]
    st.write(f"**{len(records)}** record(s)")
    if records:
        df = flatten_for_table(records)
        st.dataframe(df, use_container_width=True, hide_index=True)

        with st.expander("View raw JSON for a specific ID"):
            ids = [r.get("id") for r in records if "id" in r]
            if ids:
                chosen = st.selectbox("ID", ids, key=f"browse_id__{entity_name}")
                match = next((r for r in records if r.get("id") == chosen), None)
                st.json(match)
    else:
        st.info("No records yet, or the list couldn't be loaded.")

# ---------------- Create ----------------
if "➕ Create" in tab_map:
    with tab_map["➕ Create"]:
        st.subheader(f"Create a new {entity_name[:-1] if entity_name.endswith('s') else entity_name}")

        create_gen_key = f"create_gen__{entity_name}"
        create_gen = st.session_state.get(create_gen_key, 0)

        create_exclude = set(entity.get("create_exclude_fields", []))
        create_fields = [fld for fld in entity["fields"] if fld["name"] not in create_exclude]

        with st.form(key=f"create_form__{entity_name}__{create_gen}", clear_on_submit=True):
            values = render_form_fields(create_fields, f"create_{create_gen}")
            submitted = st.form_submit_button("Create", type="primary")
        if submitted:
            missing = [
                fld["name"] for fld in create_fields
                if fld["required"] and values.get(fld["name"]) in (None, "")
            ]
            payload, invalid = clean_payload(values)
            if missing:
                st.error(f"Missing required field(s): {', '.join(missing)}")
            elif invalid:
                st.error(f"Fix invalid JSON field(s): {', '.join(invalid)}")
            else:
                try:
                    result = client.create(endpoint, payload)
                    st.success(f"Created successfully (id={result.get('id') if result else '?'})")
                    st.json(result)
                    st.session_state.pop(f"list_cache__{entity_name}", None)
                    st.session_state[create_gen_key] = create_gen + 1
                    st.rerun()
                except APIError as e:
                    st.error(f"API error {e.status_code}: {e.detail}")
                except Exception as e:
                    st.error(f"Request failed: {e}")
                    
# ---------------- Update ----------------
if "✏️ Update" in tab_map:
    with tab_map["✏️ Update"]:
        st.subheader(f"Update an existing {entity_name[:-1] if entity_name.endswith('s') else entity_name}")
        lookup_id = st.number_input("Record ID to load", min_value=1, step=1, key=f"update_lookup__{entity_name}")
        col_load, _ = st.columns([1, 4])
        if col_load.button("Load record", key=f"load_btn__{entity_name}"):
            try:
                st.session_state[f"update_record__{entity_name}"] = client.get(endpoint, int(lookup_id))
            except APIError as e:
                st.error(f"API error {e.status_code}: {e.detail}")
                st.session_state.pop(f"update_record__{entity_name}", None)
            except Exception as e:
                st.error(f"Request failed: {e}")

        record = st.session_state.get(f"update_record__{entity_name}")
        if record:
            st.caption("Loaded record — edit fields below, then Save.")
            update_key_prefix = f"update_{record['id']}"
            with st.form(key=f"update_form__{entity_name}__{record['id']}"):
                update_exclude = set(entity.get("update_exclude_fields", []))
                update_fields = [
                    fld for fld in entity["fields"] if fld["name"] not in update_exclude
                ] + entity.get("extra_update_fields", [])
                values = render_form_fields(update_fields, update_key_prefix, record=record, force_optional=True)
                submitted = st.form_submit_button("Save changes", type="primary")
            if submitted:
                payload, invalid = clean_payload(values)
                if invalid:
                    st.error(f"Fix invalid JSON field(s): {', '.join(invalid)}")
                elif not payload:
                    st.warning("No changes to save.")
                else:
                    try:
                        result = client.update(endpoint, record["id"], payload)
                        st.success("Updated successfully.")
                        st.json(result)
                        st.session_state.pop(f"list_cache__{entity_name}", None)
                        st.session_state[f"update_record__{entity_name}"] = result
                    except APIError as e:
                        st.error(f"API error {e.status_code}: {e.detail}")
                    except Exception as e:
                        st.error(f"Request failed: {e}")

# ---------------- Delete ----------------
if "🗑️ Delete" in tab_map:
    with tab_map["🗑️ Delete"]:
        st.subheader(f"Delete a {entity_name[:-1] if entity_name.endswith('s') else entity_name}")
        del_id = st.number_input("Record ID to delete", min_value=1, step=1, key=f"delete_lookup__{entity_name}")

        preview_col, _ = st.columns([1, 4])
        if preview_col.button("Preview record", key=f"preview_btn__{entity_name}"):
            try:
                st.session_state[f"delete_preview__{entity_name}"] = client.get(endpoint, int(del_id))
            except APIError as e:
                st.error(f"API error {e.status_code}: {e.detail}")
                st.session_state.pop(f"delete_preview__{entity_name}", None)
            except Exception as e:
                st.error(f"Request failed: {e}")

        preview = st.session_state.get(f"delete_preview__{entity_name}")
        if preview:
            st.json(preview)
            confirm = st.checkbox("I understand this action is permanent", key=f"confirm_del__{entity_name}")
            if st.button("Delete permanently", type="primary", disabled=not confirm, key=f"delete_btn__{entity_name}"):
                try:
                    client.delete(endpoint, preview["id"])
                    st.success(f"Deleted record {preview['id']}.")
                    st.session_state.pop(f"delete_preview__{entity_name}", None)
                    st.session_state.pop(f"list_cache__{entity_name}", None)
                except APIError as e:
                    st.error(f"API error {e.status_code}: {e.detail}")
                except Exception as e:
                    st.error(f"Request failed: {e}")
