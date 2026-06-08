from typing import Any, Optional

from tests.clients.api_client import ApiResponse, BaseApiClient
from tests.config.settings import TestSettings


class AuthClient(BaseApiClient):
    def register(self, email: str, password: str, full_name: str) -> ApiResponse:
        payload = {"email": email, "password": password, "full_name": full_name}
        return self.post("/auth/register", json=payload)

    def login(self, email: str, password: str) -> ApiResponse:
        payload = {"email": email, "password": password}
        return self.post("/auth/login", json=payload)

    def login_and_set_token(self, email: str, password: str) -> str:
        response = self.login(email, password)
        if response.status_code != 200 or not response.json:
            raise RuntimeError(f"Login failed: {response.status_code} {response.text}")
        token = response.json["access_token"]
        self.set_token(token)
        return token


class UsersClient(BaseApiClient):
    def get_me(self) -> ApiResponse:
        return self.get("/users/me")


class ItemsClient(BaseApiClient):
    def create(self, title: str, description: Optional[str] = None) -> ApiResponse:
        payload: dict[str, Any] = {"title": title}
        if description is not None:
            payload["description"] = description
        return self.post("/items", json=payload)

    def list_items(self) -> ApiResponse:
        return self.get("/items")

    def get_item(self, item_id: int) -> ApiResponse:
        return self.get(f"/items/{item_id}")

    def update_item(
        self,
        item_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> ApiResponse:
        payload: dict[str, Any] = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        return self.put(f"/items/{item_id}", json=payload)

    def delete_item(self, item_id: int) -> ApiResponse:
        return self.delete(f"/items/{item_id}")


class HealthClient(BaseApiClient):
    def health(self) -> ApiResponse:
        return self.get("/health")

    def ready(self) -> ApiResponse:
        return self.get("/ready")


def build_clients(settings: TestSettings, token: Optional[str] = None) -> dict:
    return {
        "auth": AuthClient(settings, token=token),
        "users": UsersClient(settings, token=token),
        "items": ItemsClient(settings, token=token),
        "health": HealthClient(settings, token=token),
        "api": BaseApiClient(settings, token=token),
    }
