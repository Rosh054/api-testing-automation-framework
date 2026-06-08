from tests.helpers.assertions import assert_json_schema, assert_status_code


def test_get_current_user(authenticated_users_client, registered_user):
    response = authenticated_users_client.get_me()

    assert_status_code(response, 200)
    assert_json_schema(response, "user_schema.json")
    assert response.json["email"] == registered_user["email"]
    assert response.json["id"] == registered_user["user_id"]


def test_reject_invalid_token(settings):
    from tests.clients.auth_client import UsersClient

    client = UsersClient(settings, token="invalid.token.value")
    response = client.get_me()

    assert_status_code(response, 401)
    assert_json_schema(response, "error_schema.json")
