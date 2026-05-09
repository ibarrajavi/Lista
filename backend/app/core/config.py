# --- Third-party
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 15
    JWT_REFRESH_EXPIRY_DAYS: int = 30
    JWT_LEEWAY: int = 10
    TOKEN_BYTES: int = 32
    TOKEN_TTL_MIN: int = 30
    CORS_ORIGINS: list[str] = []


settings = Settings()
