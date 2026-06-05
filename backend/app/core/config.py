from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_base_url: str = "http://localhost:8000"
    frontend_base_url: str = "http://localhost:3000"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/security_posture"
    redis_url: str = "redis://localhost:6379/0"
    session_secret: str = "dev-session-secret-change-me"
    encryption_key: str = "vPcUrpkzqGQm_q0DVzN2ygNwb1lEWOtSyaOPafF-76k="
    github_client_id: str = ""
    github_client_secret: str = ""
    github_oauth_scopes: str = "read:user,repo"
    scorecard_binary: str = "scorecard"
    scorecard_use_stub: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
