import json
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

SCHEMAS_DIR = Path(__file__).resolve().parents[1] / "schemas"


def load_schema(schema_name: str) -> dict[str, Any]:
    schema_path = SCHEMAS_DIR / schema_name
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(data: Any, schema_name: str) -> list[str]:
    schema = load_schema(schema_name)
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    return [f"{list(error.path)}: {error.message}" for error in errors]


def assert_status_code(response, expected: int) -> None:
    assert response.status_code == expected, (
        f"Expected status {expected}, got {response.status_code}. Body: {response.text}"
    )


def assert_json_schema(response, schema_name: str) -> None:
    assert response.json is not None, "Response body is not valid JSON"
    errors = validate_schema(response.json, schema_name)
    assert not errors, f"Schema validation failed for {schema_name}:\n" + "\n".join(errors)


def assert_error_detail(response, expected_fragment: str) -> None:
    assert response.json is not None, "Expected JSON error response"
    detail = response.json.get("detail")
    if isinstance(detail, list):
        detail_text = json.dumps(detail)
    else:
        detail_text = str(detail)
    assert expected_fragment.lower() in detail_text.lower(), (
        f"Expected error containing '{expected_fragment}', got: {detail_text}"
    )
