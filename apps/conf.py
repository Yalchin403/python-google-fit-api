from functools import lru_cache
import os
import pathlib
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # pragma: no cover
    model_config = SettingsConfigDict(
        env_file=".envs/.local", env_file_encoding="utf-8", extra="allow"
    )
    API_PREFIX: str = os.getenv("API_PREFIX", "")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "LOCAL")
    DATABASE_URL: str = (
        "postgresql://fitdbadmin:fitdbadminpassword12@postgres:5432/fitdb"
    )
    LOG_CONFIG: dict[str, Any] = {
        "logger": {
            "path": "./logs/access.log",
            "level": "info",
            "rotation": "20 days",
            "retention": "1 months",
            "format": "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> request id:"
            "{extra[request_id]} - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        }
    }
    GOOGLE_CLIENT_ID: str = "googleClientId"
    GOOGLE_CLIENT_SECRET: str = "googleClientSecret"
    GOOGLE_ACCESS_TOKEN_URL: str = "https://accounts.google.com/o/oauth2/token"
    GOOGLE_REDIRECT_URL: str = "http://localhost:8000/auth/google/callback"
    GOOGLE_SCOPES: list = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
        "https://www.googleapis.com/auth/fitness.activity.read",
        "https://www.googleapis.com/auth/fitness.body.read",
        "https://www.googleapis.com/auth/fitness.body_temperature.read",
        "https://www.googleapis.com/auth/fitness.heart_rate.read",
        "https://www.googleapis.com/auth/fitness.location.read",
        "https://www.googleapis.com/auth/fitness.sleep.read",
    ]
    GOOGLE_CLIENT_SECRET_FILE: str = os.path.join(
        pathlib.Path(__file__).parent, "client_secret.json"
    )
    DASHBOARD_URL: str = "/dashboard"


@lru_cache()  # pragma: no cover
def get_settings() -> Settings:
    return Settings()
