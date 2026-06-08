from tests.helpers.assertions import assert_status_code
from tests.helpers.data_factory import build_user_payload, random_item_payload


def test_user_persisted_in_database(auth_client, db_helper):
    payload = build_user_payload()
    response = auth_client.register(**payload)

    assert_status_code(response, 201)
    db_user = db_helper.get_user_by_email(payload["email"])
    assert db_user is not None
    assert db_user["email"] == payload["email"]
    assert db_user["full_name"] == payload["full_name"]
    assert db_user["is_active"] is True


def test_item_persisted_in_database(authenticated_items_client, db_helper, registered_user):
    payload = random_item_payload("DB Item")
    response = authenticated_items_client.create(**payload)

    assert_status_code(response, 201)
    item_id = response.json["id"]
    db_item = db_helper.get_item_by_id(item_id)

    assert db_item is not None
    assert db_item["title"] == payload["title"]
    assert db_item["owner_id"] == registered_user["user_id"]
    assert db_item["is_deleted"] is False


def test_deleted_item_marked_in_database(authenticated_items_client, db_helper):
    created = authenticated_items_client.create(title="Soft Delete Check")
    item_id = created.json["id"]

    delete_response = authenticated_items_client.delete_item(item_id)
    assert_status_code(delete_response, 204)

    db_item = db_helper.get_item_by_id(item_id)
    assert db_item is not None
    assert db_item["is_deleted"] is True
