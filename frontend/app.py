

import json
from datetime import date, datetime

import pandas as pd
import streamlit as st

from api_client import APIClient, APIError
from entities import ENTITIES, ENUMS, CATEGORY_ORDER
from auth_gate import render_gate, render_sidebar_identity
import autocheck_view

st.set_page_config(page_title="Travel Assistance API Console", page_icon="🧳", layout="wide")

# --------------------------------------------------------------------------
# Connection settings (kept outside the auth gate so the URL survives login)
# --------------------------------------------------------------------------
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

# --------------------------------------------------------------------------
# Role selection -> login -> authenticated client
# --------------------------------------------------------------------------
client = render_gate(st.session_state.base_url)
if client is None:
    st.stop()

render_sidebar_identity()

# --------------------------------------------------------------------------
# Client role: hand off entirely to the traveller compliance-check view.
# --------------------------------------------------------------------------
if st.session_state.get("auth_role") == "client":
    autocheck_view.render_autocheck(client)
    st.stop()

# --------------------------------------------------------------------------
# Admin role: CRUD dashboard below.
# --------------------------------------------------------------------------
with st.sidebar:
    st.divider()
    st.caption("ENTITY")

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
                # nested response object (e.g. country: {...}) -> pull a display field
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
        with st.form(key=f"create_form__{entity_name}"):
            values = render_form_fields(entity["fields"], "create")
            submitted = st.form_submit_button("Create", type="primary")
        if submitted:
            missing = [
                fld["name"] for fld in entity["fields"]
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
            with st.form(key=f"update_form__{entity_name}"):
                update_fields = entity["fields"] + entity.get("extra_update_fields", [])
                values = render_form_fields(update_fields, "update", record=record, force_optional=True)
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
