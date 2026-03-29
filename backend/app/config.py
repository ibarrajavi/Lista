from pydantic_settings import BaseSettings, SettingsConfigDict

"""
Key fields:
- DATABASE_URL: URL for the todo_app PostgreSQL database.
"""

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    DATABASE_URL: str

settings = Settings()
