from typing import Any, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from tests.config.settings import TestSettings


class DatabaseHelper:
    def __init__(self, settings: TestSettings):
        self.settings = settings
        self.engine = create_engine(settings.database_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def fetch_one(self, query: str, params: Optional[dict[str, Any]] = None) -> Optional[dict[str, Any]]:
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            row = result.mappings().first()
            return dict(row) if row else None

    def user_exists_by_email(self, email: str) -> bool:
        row = self.fetch_one("SELECT id, email FROM users WHERE email = :email", {"email": email})
        return row is not None

    def get_user_by_email(self, email: str) -> Optional[dict[str, Any]]:
        return self.fetch_one(
            "SELECT id, email, full_name, is_active FROM users WHERE email = :email",
            {"email": email},
        )

    def get_item_by_id(self, item_id: int) -> Optional[dict[str, Any]]:
        return self.fetch_one(
            "SELECT id, title, description, owner_id, is_deleted FROM items WHERE id = :item_id",
            {"item_id": item_id},
        )

    def item_is_deleted(self, item_id: int) -> bool:
        row = self.get_item_by_id(item_id)
        return bool(row and row.get("is_deleted"))
