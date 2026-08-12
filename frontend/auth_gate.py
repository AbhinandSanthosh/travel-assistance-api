"""
Landing / auth gate for the Travel Assistance console.

Flow:
    1. Role selection: Admin  vs.  Client
    2. Admin  -> username + password  -> POST /api/v1/auth/login (JWT)
       Client -> API key               -> stored for use on /autocheck

`render_gate(base_url)` returns an `APIClient` once the user is fully
authenticated for their chosen role, or None (and renders the
appropriate screen itself) if the gate isn't cleared yet -- callers
should stop rendering the rest of the page when None comes back.
"""

import streamlit as st

from api_client import APIClient, APIError

SESSION_ROLE = "auth_role"                 # "admin" | "client" | None
SESSION_ADMIN_TOKEN = "auth_admin_token"
SESSION_ADMIN_USER = "auth_admin_user"
SESSION_CLIENT_API_KEY = "auth_client_api_key"

# Client-portal-specific session state (separate from the API key
# itself -- a portal token proves "you're an authorized contact for
# this company" and can manage/generate keys, but can never be used
# against /autocheck).
SESSION_CLIENT_PORTAL_TOKEN = "auth_client_portal_token"
SESSION_CLIENT_ENTRY_MODE = "auth_client_entry_mode"  # "have_key" | "portal"
SESSION_CLIENT_PORTAL_VIEW = "auth_client_portal_view"  # "login" | "signup"


def _reset_session():
    for key in (
        SESSION_ROLE,
        SESSION_ADMIN_TOKEN,
        SESSION_ADMIN_USER,
        SESSION_CLIENT_API_KEY,
        SESSION_CLIENT_PORTAL_TOKEN,
        SESSION_CLIENT_ENTRY_MODE,
        SESSION_CLIENT_PORTAL_VIEW,
    ):
        st.session_state.pop(key, None)
    # entity list caches etc. shouldn't leak across sessions/roles either
    for key in list(st.session_state.keys()):
        if key.startswith("list_cache__") or key.startswith("autocheck_"):
            st.session_state.pop(key, None)


def is_authenticated() -> bool:
    role = st.session_state.get(SESSION_ROLE)
    if role == "admin":
        return bool(st.session_state.get(SESSION_ADMIN_TOKEN))
    if role == "client":
        return bool(st.session_state.get(SESSION_CLIENT_API_KEY))
    return False


def render_sidebar_identity():
    """Shows who's logged in + a logout button. Call from the sidebar
    once authenticated."""
    role = st.session_state.get(SESSION_ROLE)

    st.sidebar.divider()
    if role == "admin":
        user = st.session_state.get(SESSION_ADMIN_USER) or {}
        st.sidebar.caption("Signed in as ADMIN")
        st.sidebar.markdown(f"**{user.get('full_name', user.get('username', 'Admin'))}**")
        if user.get("role_name"):
            st.sidebar.caption(user["role_name"])
    elif role == "client":
        st.sidebar.caption("Signed in as CLIENT")
        key = st.session_state.get(SESSION_CLIENT_API_KEY, "")
        masked = f"{key[:4]}{'•' * max(len(key) - 4, 0)}" if key else ""
        st.sidebar.markdown(f"`{masked}`")

    if st.sidebar.button("🚪 Log out", use_container_width=True):
        _reset_session()
        st.rerun()


def _render_role_selection():
    st.title("🧳 Travel Assistance API")
    st.caption("Choose how you'd like to sign in.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛡️ Admin")
        st.write("Manage reference data, compliance rules, and rule versioning/approvals.")
        if st.button("Continue as Admin", use_container_width=True, type="primary"):
            st.session_state[SESSION_ROLE] = "admin"
            st.rerun()
    with col2:
        st.subheader("✈️ Client")
        st.write("Run a compliance check for a traveller using your API key.")
        if st.button("Continue as Client", use_container_width=True, type="primary"):
            st.session_state[SESSION_ROLE] = "client"
            st.rerun()


def _render_admin_login(base_url: str):
    st.title("🛡️ Admin Login")

    if st.button("← Back"):
        _reset_session()
        st.rerun()

    with st.form("admin_login_form"):
        username = st.text_input("Username or email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", type="primary")

    if submitted:
        if not username or not password:
            st.warning("Enter both a username and a password.")
            return

        client = APIClient(base_url)
        try:
            with st.spinner("Signing in..."):
                result = client.login(username, password)
            token = result["accessToken"]
            st.session_state[SESSION_ADMIN_TOKEN] = token

            authed_client = APIClient(base_url, token=token)
            try:
                st.session_state[SESSION_ADMIN_USER] = authed_client.me()
            except Exception:
                # Non-fatal -- login succeeded even if /me can't be shown.
                st.session_state[SESSION_ADMIN_USER] = {"username": username}

            st.rerun()
        except APIError as e:
            if e.status_code == 401:
                st.error("Invalid username or password.")
            elif e.status_code == 403:
                st.error("This account is inactive. Contact your administrator.")
            else:
                st.error(f"API error {e.status_code}: {e.detail}")
        except Exception as e:
            st.error(f"Could not reach API at {base_url}. {e}")


def _render_client_login(base_url: str):
    st.title("✈️ Client Access")

    if st.button("← Back"):
        _reset_session()
        st.rerun()

    mode = st.session_state.get(SESSION_CLIENT_ENTRY_MODE)

    if mode is None:
        st.write("How would you like to continue?")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔑 I have an API key")
            st.write("Already have a key from your dashboard? Use it directly.")
            if st.button("Continue with API key", use_container_width=True, type="primary"):
                st.session_state[SESSION_CLIENT_ENTRY_MODE] = "have_key"
                st.rerun()
        with col2:
            st.subheader("👤 Developer portal")
            st.write("Sign up, log in, and generate an API key for your organisation.")
            if st.button("Continue to portal", use_container_width=True, type="primary"):
                st.session_state[SESSION_CLIENT_ENTRY_MODE] = "portal"
                st.session_state[SESSION_CLIENT_PORTAL_VIEW] = "login"
                st.rerun()
        return

    if st.button("← Choose a different option"):
        st.session_state.pop(SESSION_CLIENT_ENTRY_MODE, None)
        st.session_state.pop(SESSION_CLIENT_PORTAL_VIEW, None)
        st.rerun()

    if mode == "have_key":
        _render_client_api_key_entry(base_url)
    elif mode == "portal":
        _render_client_portal(base_url)


def _render_client_api_key_entry(base_url: str):
    st.write("Enter the API key issued to your organisation to run compliance checks.")

    with st.form("client_login_form"):
        api_key = st.text_input("API key", type="password")
        submitted = st.form_submit_button("Continue", type="primary")

    if submitted:
        if not api_key.strip():
            st.warning("Enter an API key.")
            return

        key = api_key.strip()
        client = APIClient(base_url)
        try:
            with st.spinner("Validating API key..."):
                client.validate_api_key(key)
            st.session_state[SESSION_CLIENT_API_KEY] = key
            st.rerun()
        except APIError as e:
            if e.status_code == 401:
                st.error("Invalid API key.")
            elif e.status_code == 403:
                st.error(e.detail)
            else:
                st.error(f"API error {e.status_code}: {e.detail}")
        except Exception as e:
            st.error(f"Could not reach API at {base_url}. {e}")


def _render_client_portal(base_url: str):
    """Developer portal: sign up, log in, then generate/view an API
    key from a small dashboard. Mirrors how Stripe/Twilio/OpenAI
    separate 'having an account' from 'having a live secret'."""

    portal_token = st.session_state.get(SESSION_CLIENT_PORTAL_TOKEN)
    if portal_token:
        _render_client_portal_dashboard(base_url, portal_token)
        return

    view = st.session_state.get(SESSION_CLIENT_PORTAL_VIEW, "login")
    tab_login, tab_signup = st.tabs(["Log in", "Create account"])

    with tab_login:
        with st.form("portal_login_form"):
            email = st.text_input("Contact email", key="portal_login_email")
            password = st.text_input("Password", type="password", key="portal_login_password")
            submitted = st.form_submit_button("Log in", type="primary")

        if submitted:
            if not email.strip() or not password:
                st.warning("Enter both an email and a password.")
            else:
                client = APIClient(base_url)
                try:
                    with st.spinner("Signing in..."):
                        result = client.client_login(email.strip(), password)
                    st.session_state[SESSION_CLIENT_PORTAL_TOKEN] = result["accessToken"]
                    st.rerun()
                except APIError as e:
                    if e.status_code == 401:
                        st.error("Invalid email or password.")
                    elif e.status_code == 403:
                        st.error(e.detail)
                    else:
                        st.error(f"API error {e.status_code}: {e.detail}")
                except Exception as e:
                    st.error(f"Could not reach API at {base_url}. {e}")

    with tab_signup:
        st.caption("Creates your account only -- you'll generate an API key after logging in.")
        with st.form("portal_signup_form"):
            company_name = st.text_input("Company name")
            client_name = st.text_input("Your name")
            contact_email = st.text_input("Contact email", key="portal_signup_email")
            contact_phone = st.text_input("Phone (optional)")
            password = st.text_input(
                "Password", type="password", key="portal_signup_password",
                help="At least 8 characters.",
            )
            submitted = st.form_submit_button("Create account", type="primary")

        if submitted:
            if not all([company_name.strip(), client_name.strip(), contact_email.strip(), password]):
                st.warning("Fill in company name, your name, email, and a password.")
            elif len(password) < 8:
                st.warning("Password must be at least 8 characters.")
            else:
                client = APIClient(base_url)
                try:
                    with st.spinner("Creating account..."):
                        client.client_signup(
                            company_name=company_name.strip(),
                            client_name=client_name.strip(),
                            contact_email=contact_email.strip(),
                            password=password,
                            contact_phone=contact_phone.strip() or None,
                        )
                    st.success("Account created! Log in on the 'Log in' tab to generate your API key.")
                except APIError as e:
                    if e.status_code == 409:
                        st.error(e.detail)
                    else:
                        st.error(f"API error {e.status_code}: {e.detail}")
                except Exception as e:
                    st.error(f"Could not reach API at {base_url}. {e}")


def _render_client_portal_dashboard(base_url: str, portal_token: str):
    st.subheader("👤 Developer Portal")

    if st.button("Log out of portal"):
        st.session_state.pop(SESSION_CLIENT_PORTAL_TOKEN, None)
        st.rerun()

    client = APIClient(base_url)
    try:
        status_info = client.client_api_key_status(portal_token)
    except APIError as e:
        st.error(f"Could not load key status: {e.detail}")
        return

    if status_info.get("has_active_key"):
        st.info(f"Active key: `{status_info['masked_key']}`")
        st.caption(
            "The full key was shown once, at generation time, and can't be "
            "retrieved again -- rotate if it's been lost."
        )
    else:
        st.warning("No active API key yet.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate new key (rotates any existing key)", type="primary"):
            try:
                with st.spinner("Generating key..."):
                    result = client.generate_client_api_key(portal_token)
                st.session_state["_generated_key_display"] = result
                st.rerun()
            except APIError as e:
                st.error(f"Could not generate key: {e.detail}")
    with col2:
        if status_info.get("has_active_key") and st.button("Revoke current key"):
            try:
                client.revoke_client_api_key(portal_token)
                st.session_state.pop("_generated_key_display", None)
                st.rerun()
            except APIError as e:
                st.error(f"Could not revoke key: {e.detail}")

    generated = st.session_state.get("_generated_key_display")
    if generated:
        st.success("New API key generated -- copy it now, it won't be shown again.")
        st.code(generated["api_key"], language=None)
        if st.button("Use this key to run compliance checks now", type="primary"):
            st.session_state[SESSION_CLIENT_API_KEY] = generated["api_key"]
            st.session_state.pop("_generated_key_display", None)
            st.rerun()


def render_gate(base_url: str) -> APIClient | None:
    """Renders whichever screen is needed next. Returns a ready-to-use
    APIClient once authenticated, else None (caller should st.stop()
    or simply return after this)."""

    role = st.session_state.get(SESSION_ROLE)

    if role is None:
        _render_role_selection()
        return None

    if role == "admin":
        if not st.session_state.get(SESSION_ADMIN_TOKEN):
            _render_admin_login(base_url)
            return None
        return APIClient(base_url, token=st.session_state[SESSION_ADMIN_TOKEN])

    if role == "client":
        if not st.session_state.get(SESSION_CLIENT_API_KEY):
            _render_client_login(base_url)
            return None
        return APIClient(base_url)

    # Unknown role in session state somehow -- reset and start over.
    _reset_session()
    st.rerun()
    return None