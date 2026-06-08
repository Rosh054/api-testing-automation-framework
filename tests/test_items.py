from tests.helpers.assertions import assert_json_schema, assert_status_code
from tests.helpers.data_factory import load_test_data


def test_create_item(authenticated_items_client, db_helper):
    payload = load_test_data("test_items.json")["valid_item"]
    response = authenticated_items_client.create(**payload)

    assert_status_code(response, 201)
    assert_json_schema(response, "item_schema.json")

    item_id = response.json["id"]
    db_item = db_helper.get_item_by_id(item_id)
    assert db_item is not None
    assert db_item["title"] == payload["title"]
    assert db_item["is_deleted"] is False


def test_get_item(authenticated_items_client):
    created = authenticated_items_client.create(title="Get Item Test", description="detail")
    item_id = created.json["id"]

    response = authenticated_items_client.get_item(item_id)

    assert_status_code(response, 200)
    assert_json_schema(response, "item_schema.json")
    assert response.json["id"] == item_id


def test_list_items(authenticated_items_client):
    authenticated_items_client.create(title="List Item A")
    authenticated_items_client.create(title="List Item B")

    response = authenticated_items_client.list_items()

    assert_status_code(response, 200)
    assert isinstance(response.json, list)
    assert len(response.json) >= 2
    for item in response.json:
        errors = []
        from tests.helpers.assertions import validate_schema

        errors.extend(validate_schema(item, "item_schema.json"))
        assert not errors


def test_update_item(authenticated_items_client):
    created = authenticated_items_client.create(title="Original Title", description="old")
    item_id = created.json["id"]
    updated_payload = load_test_data("test_items.json")["updated_item"]

    response = authenticated_items_client.update_item(item_id, **updated_payload)

    assert_status_code(response, 200)
    assert_json_schema(response, "item_schema.json")
    assert response.json["title"] == updated_payload["title"]
    assert response.json["description"] == updated_payload["description"]


def test_delete_item(authenticated_items_client, db_helper):
    created = authenticated_items_client.create(title="Delete Me")
    item_id = created.json["id"]

    delete_response = authenticated_items_client.delete_item(item_id)
    assert_status_code(delete_response, 204)

    get_response = authenticated_items_client.get_item(item_id)
    assert_status_code(get_response, 404)
    assert db_helper.item_is_deleted(item_id)
