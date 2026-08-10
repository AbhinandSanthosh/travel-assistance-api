import requests


class APIError(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"[{status_code}] {detail}")


def _handle(resp: requests.Response):
    if resp.status_code >= 400:
        try:
            detail = resp.json().get("detail", resp.text)
        except Exception:
            detail = resp.text
        raise APIError(resp.status_code, detail)
    if resp.status_code == 204 or not resp.content:
        return None
    return resp.json()


class APIClient:
    """Thin REST client for the Travel Assistance API console.

    Admin (CRUD/rule-management) endpoints require a Bearer JWT obtained
    from POST /api/v1/auth/login -- pass it in as `token` (or call
    .login() then reuse the returned token). The /autocheck endpoint
    used by the client flow does NOT use this token; it authenticates
    via an api_key field in the request body instead.
    """

    def __init__(self, base_url: str, token: str | None = None, timeout: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _headers(self) -> dict:
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    # ------------------------------------------------------------------
    # Admin auth
    # ------------------------------------------------------------------

    def login(self, username: str, password: str) -> dict:
        """POST /api/v1/auth/login. Returns the parsed JSON body
        (accessToken / tokenType / expiresIn) -- does not mutate
        self.token, callers should store the token in session state
        themselves.
        """
        resp = requests.post(
            self._url("/api/v1/auth/login"),
            json={"username": username, "password": password},
            timeout=self.timeout,
        )
        return _handle(resp)

    def me(self) -> dict:
        """GET /api/v1/auth/me using the current bearer token."""
        resp = requests.get(
            self._url("/api/v1/auth/me"),
            headers=self._headers(),
            timeout=self.timeout,
        )
        return _handle(resp)

    # ------------------------------------------------------------------
    # Generic CRUD (admin, bearer-token protected)
    # ------------------------------------------------------------------

    def list(self, path: str):
        resp = requests.get(self._url(path), headers=self._headers(), timeout=self.timeout)
        return _handle(resp)

    def get(self, path: str, item_id):
        clean = path.rstrip("/")
        resp = requests.get(
            f"{self._url(clean)}/{item_id}", headers=self._headers(), timeout=self.timeout
        )
        return _handle(resp)

    def create(self, path: str, payload: dict, extra_headers: dict | None = None):
        headers = self._headers()
        if extra_headers:
            headers = {**headers, **extra_headers}
        resp = requests.post(
            self._url(path), json=payload, headers=headers, timeout=self.timeout
        )
        return _handle(resp)

    # ------------------------------------------------------------------
    # Client (API key) auth
    # ------------------------------------------------------------------

    def validate_api_key(self, api_key: str) -> dict:
        """POST /autocheck/validate-key. Confirms the key is valid,
        active, and whitelisted for the caller's IP -- without running
        a full compliance check or counting against the client's rate
        limit. Raises APIError (401/403) if the key doesn't check out."""
        resp = requests.post(
            self._url("/autocheck/validate-key"),
            headers={"X-API-Key": api_key},
            timeout=self.timeout,
        )
        return _handle(resp)

    def update(self, path: str, item_id, payload: dict):
        clean = path.rstrip("/")
        resp = requests.put(
            f"{self._url(clean)}/{item_id}",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout,
        )
        return _handle(resp)

    def delete(self, path: str, item_id):
        clean = path.rstrip("/")
        resp = requests.delete(
            f"{self._url(clean)}/{item_id}", headers=self._headers(), timeout=self.timeout
        )
        return _handle(resp)

    def health(self):
        resp = requests.get(self._url("/health"), timeout=self.timeout)
        return _handle(resp)