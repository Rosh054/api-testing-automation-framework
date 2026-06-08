# How to Extend This Framework

Use this guide to adapt the framework to another FastAPI or REST project.

## 1. Change Base URL and Environment

Copy `.env.example` to `.env` and update:

```env
BASE_URL=http://localhost:9000
DATABASE_URL=postgresql://user:pass@localhost:5432/your_db
ENVIRONMENT=local
```

`tests/config/settings.py` loads these values automatically.

## 2. Add a New API Client

Create a client in `tests/clients/`:

```python
from tests.clients.api_client import BaseApiClient

class OrdersClient(BaseApiClient):
    def create_order(self, product_id: int, quantity: int):
        return self.post("/orders", json={"product_id": product_id, "quantity": quantity})
```

Register it in `build_clients()` inside `tests/clients/auth_client.py`.

## 3. Add JSON Schemas

Add a schema file under `tests/schemas/`, then validate in tests:

```python
from tests.helpers.assertions import assert_json_schema

assert_json_schema(response, "order_schema.json")
```

## 4. Add Test Data and Factories

- Static fixtures: `tests/data/orders.json`
- Dynamic data: extend `tests/helpers/data_factory.py`

```python
def random_order_payload():
    return {"product_id": 1, "quantity": 2}
```

## 5. Add Test Files

Create `tests/test_orders.py` and use fixtures from `conftest.py`:

```python
def test_create_order(authenticated_orders_client):
    response = authenticated_orders_client.create_order(product_id=1, quantity=1)
    assert response.status_code == 201
```

## 6. Configure Authentication

If your API uses a different auth flow:

1. Update `AuthClient.login()` path and response parsing
2. Update `registered_user` fixture token extraction
3. Adjust `BaseApiClient._build_headers()` if token format differs

For API keys:

```python
headers["X-API-Key"] = self.settings.api_key
```

## 7. Add Database Helpers

Extend `tests/helpers/db_helpers.py` with queries for your tables.

## 8. Wire CI

Update `.github/workflows/api-tests.yml` service startup commands if your target API lives in another compose file.

## Checklist for a New Service

- [ ] Update `.env` values
- [ ] Add or modify clients
- [ ] Add schemas for each response contract
- [ ] Add positive, negative, and DB validation tests
- [ ] Confirm `make test` passes locally
- [ ] Push and verify GitHub Actions
