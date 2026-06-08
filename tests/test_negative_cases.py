from tests.helpers.assertions import assert_json_schema, assert_status_code


def test_invalid_payload_missing_required_fields(auth_client):
    response = auth_client.post("/auth/register", json={"email": "missing-fields@example.com"})

    assert_status_code(response, 422)
    assert_json_schema(response, "error_schema.json")


def test_unauthorized_item_create(api_clients):
    payload = {"title": "Unauthorized Item"}
    response = api_clients["items"].create(**payload)

    assert_status_code(response, 401)
    assert_json_schema(response, "error_schema.json")


def test_invalid_item_id(authenticated_items_client):
    response = authenticated_items_client.get_item(999999)

    assert_status_code(response, 404)
    assert_json_schema(response, "error_schema.json")


def test_duplicate_user_registration(auth_client):
    from tests.helpers.data_factory import unique_email

    email = unique_email("neg-dup")
    payload = {"email": email, "password": "SecurePass123!", "full_name": "Dup User"}

    first = auth_client.register(**payload)
    second = auth_client.register(**payload)

    assert_status_code(first, 201)
    assert_status_code(second, 409)


def test_invalid_login_credentials(auth_client):
    response = auth_client.login("nobody@example.com", "BadPassword1!")

    assert_status_code(response, 401)
    assert_json_schema(response, "error_schema.json")
