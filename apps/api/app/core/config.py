from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    app_name: str = "Enterprise Knowledge Assistant"
    app_version: str = "1.0.0"
    environment: str = Field(
        default="development",
        validation_alias=AliasChoices("ENVIRONMENT", "APP_ENV"),
    )

    frontend_url: str = Field(
        default="http://localhost:3000",
        validation_alias=AliasChoices("FRONTEND_URL", "WEB_URL"),
    )

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    groq_api_key: str = Field(
        validation_alias=AliasChoices("GROQ_API_KEY", "API_KEY"),
    )
    llm_model: str = Field(
        default="gpt-4o-mini",
        validation_alias=AliasChoices("LLM_MODEL", "MODEL"),
    )

    llm_max_tokens: str = Field(
        default=500, validation_alias=AliasChoices("LLM_MAX_TOKENS", "MAX_TOKENS")
    )

    llm_temperature: str = Field(
        default=0.7, validation_alias=AliasChoices("LLM_TEMPERATURE", "TEMPERATURE")
    )

    supabase_url: str = Field("SUPABASE_URL")

    supabase_key: str = Field("SUPABASE_KEY")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
