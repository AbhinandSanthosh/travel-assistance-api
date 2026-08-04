
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
    def __init__(self, base_url: str, timeout: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def list(self, path: str):
        resp = requests.get(self._url(path), timeout=self.timeout)
        return _handle(resp)

    def get(self, path: str, item_id):
        clean = path.rstrip("/")
        resp = requests.get(f"{self._url(clean)}/{item_id}", timeout=self.timeout)
        return _handle(resp)

    def create(self, path: str, payload: dict):
        resp = requests.post(self._url(path), json=payload, timeout=self.timeout)
        return _handle(resp)

    def update(self, path: str, item_id, payload: dict):
        clean = path.rstrip("/")
        resp = requests.put(f"{self._url(clean)}/{item_id}", json=payload, timeout=self.timeout)
        return _handle(resp)

    def delete(self, path: str, item_id):
        clean = path.rstrip("/")
        resp = requests.delete(f"{self._url(clean)}/{item_id}", timeout=self.timeout)
        return _handle(resp)

    def health(self):
        resp = requests.get(self._url("/health"), timeout=self.timeout)
        return _handle(resp)
