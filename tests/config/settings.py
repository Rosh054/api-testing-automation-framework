from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = Field(default="local", alias="ENVIRONMENT")
    base_url: str = Field(default="http://localhost:8000", alias="BASE_URL")
    database_url: str = Field(
        default="postgresql://apiuser:apipass@localhost:5432/api_test_db",
        alias="DATABASE_URL",
    )
    test_user_email: str = Field(default="testuser@example.com", alias="TEST_USER_EMAIL")
    test_user_password: str = Field(default="TestPass123!", alias="TEST_USER_PASSWORD")
    test_user_full_name: str = Field(default="Test User", alias="TEST_USER_FULL_NAME")
    request_timeout: float = Field(default=10.0, alias="REQUEST_TIMEOUT")
    jwt_secret_key: str = Field(default="dev-secret-key-change-in-production", alias="JWT_SECRET_KEY")


@lru_cache
def get_settings() -> TestSettings:
    return TestSettings()
