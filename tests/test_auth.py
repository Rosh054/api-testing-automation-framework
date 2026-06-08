from tests.helpers.assertions import assert_json_schema, assert_status_code
from tests.helpers.data_factory import build_user_payload, unique_email


def test_register_valid_user(auth_client, db_helper):
    payload = build_user_payload()
    response = auth_client.register(**payload)

    assert_status_code(response, 201)
    assert_json_schema(response, "user_schema.json")
    assert db_helper.user_exists_by_email(payload["email"])


def test_prevent_duplicate_user(auth_client):
    email = unique_email("duplicate")
    payload = build_user_payload(email=email)

    first = auth_client.register(**payload)
    second = auth_client.register(**payload)

    assert_status_code(first, 201)
    assert_status_code(second, 409)
    assert "already exists" in second.json["detail"].lower()


def test_login_valid_user(auth_client, registered_user):
    response = auth_client.login(registered_user["email"], registered_user["password"])

    assert_status_code(response, 200)
    assert "access_token" in response.json
    assert response.json["token_type"] == "bearer"


def test_reject_invalid_password(auth_client, registered_user):
    response = auth_client.login(registered_user["email"], "NotTheRightPassword1!")

    assert_status_code(response, 401)
    assert_json_schema(response, "error_schema.json")


def test_protected_route_requires_token(api_clients):
    response = api_clients["users"].get_me()

    assert_status_code(response, 401)
    assert_json_schema(response, "error_schema.json")
