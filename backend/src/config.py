"""
Phase 2 - Backend Configuration
Loads environment variables using Pydantic BaseSettings (12-factor app principle)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application configuration loaded from environment variables"""

    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # SendGrid
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # Application
    ENVIRONMENT: str = "development"
    APP_NAME: str = "Todo SaaS Platform API"
    API_VERSION: str = "v1"

    # Rate Limiting
    RATE_LIMIT_AUTH: int = 100
    RATE_LIMIT_GENERAL: int = 1000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
