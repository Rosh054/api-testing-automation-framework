from typing import Any, Optional

import httpx

from tests.config.settings import TestSettings


class ApiResponse:
    def __init__(self, response: httpx.Response):
        self.status_code = response.status_code
        self.headers = response.headers
        self.raw = response
        self._json: Optional[Any] = None

        if response.content:
            try:
                self._json = response.json()
            except ValueError:
                self._json = None
        else:
            self._json = None

    @property
    def json(self) -> Any:
        return self._json

    @property
    def text(self) -> str:
        return self.raw.text


class BaseApiClient:
    def __init__(self, settings: TestSettings, token: Optional[str] = None):
        self.settings = settings
        self.base_url = settings.base_url.rstrip("/")
        self.timeout = settings.request_timeout
        self._token = token

    def set_token(self, token: Optional[str]) -> None:
        self._token = token

    def _build_headers(self, extra_headers: Optional[dict[str, str]] = None) -> dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> ApiResponse:
        url = f"{self.base_url}{path}"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.request(
                method=method,
                url=url,
                json=json,
                params=params,
                headers=self._build_headers(headers),
            )
        return ApiResponse(response)

    def get(self, path: str, **kwargs) -> ApiResponse:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> ApiResponse:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> ApiResponse:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> ApiResponse:
        return self.request("DELETE", path, **kwargs)
