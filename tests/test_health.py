from tests.helpers.assertions import assert_status_code


def test_api_is_alive(api_clients):
    response = api_clients["health"].health()
    assert_status_code(response, 200)
    assert response.json["status"] == "ok"
    assert response.json["service"] == "sample-api"


def test_readiness_check_works(api_clients):
    response = api_clients["health"].ready()
    assert_status_code(response, 200)
    assert response.json["status"] == "ready"
    assert response.json["database"] == "connected"
