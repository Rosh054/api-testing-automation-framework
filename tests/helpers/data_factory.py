import json
import uuid
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_test_data(filename: str) -> Any:
    path = DATA_DIR / filename
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def unique_email(prefix: str = "user") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}@example.com"


def random_item_payload(prefix: str = "Item") -> dict[str, str]:
    suffix = uuid.uuid4().hex[:6]
    return {
        "title": f"{prefix} {suffix}",
        "description": f"Auto-generated description {suffix}",
    }


def build_user_payload(
    email: str | None = None,
    password: str = "TestPass123!",
    full_name: str = "Automation User",
) -> dict[str, str]:
    return {
        "email": email or unique_email(),
        "password": password,
        "full_name": full_name,
    }
