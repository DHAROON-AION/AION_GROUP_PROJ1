"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the AION AI Factory backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="AION AI Factory", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")

    ollama_base_url: str = Field(
        default="http://ollama:11434",
        alias="OLLAMA_BASE_URL",
    )
    ollama_default_model: str = Field(
        default="llama3.2:3b",
        alias="OLLAMA_DEFAULT_MODEL",
    )

    database_url: str = Field(
        default="postgresql://aion_admin:bank_secure_password_2026@postgres:5432/aion_banking",
        alias="DATABASE_URL",
    )

    langfuse_host: str = Field(
        default="http://langfuse-web:3000",
        alias="LANGFUSE_HOST",
    )
    langfuse_public_key: str = Field(default="", alias="LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key: str = Field(default="", alias="LANGFUSE_SECRET_KEY")
    langfuse_enabled: bool = Field(default=True, alias="LANGFUSE_ENABLED")

    embedding_model: str = Field(
        default="BAAI/bge-small-en-v1.5",
        alias="EMBEDDING_MODEL",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance (singleton per process)."""
    return Settings()

class Settings(BaseSettings):
    
    DATABASE_URL: str
    
    
    OLLAMA_BASE_URL: str
    OLLAMA_DEFAULT_MODEL: str
    
   
    EMBEDDING_MODEL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
