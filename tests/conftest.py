import pytest

from tests.clients.auth_client import AuthClient, ItemsClient, UsersClient, build_clients
from tests.config.settings import TestSettings, get_settings
from tests.helpers.data_factory import build_user_payload, unique_email
from tests.helpers.db_helpers import DatabaseHelper


@pytest.fixture(scope="session")
def settings() -> TestSettings:
    return get_settings()


@pytest.fixture(scope="session")
def db_helper(settings: TestSettings) -> DatabaseHelper:
    return DatabaseHelper(settings)


@pytest.fixture
def api_clients(settings: TestSettings):
    return build_clients(settings)


@pytest.fixture
def auth_client(settings: TestSettings) -> AuthClient:
    return AuthClient(settings)


@pytest.fixture
def registered_user(auth_client: AuthClient, settings: TestSettings):
    email = unique_email("automation")
    payload = build_user_payload(
        email=email,
        password=settings.test_user_password,
        full_name=settings.test_user_full_name,
    )
    response = auth_client.register(**payload)
    assert response.status_code == 201, response.text
    token = auth_client.login_and_set_token(email, settings.test_user_password)
    clients = build_clients(settings, token=token)
    return {
        "email": email,
        "password": settings.test_user_password,
        "full_name": settings.test_user_full_name,
        "token": token,
        "user_id": response.json["id"],
        "auth": clients["auth"],
        "users": clients["users"],
        "items": clients["items"],
    }


@pytest.fixture
def authenticated_items_client(registered_user) -> ItemsClient:
    return registered_user["items"]


@pytest.fixture
def authenticated_users_client(registered_user) -> UsersClient:
    return registered_user["users"]
