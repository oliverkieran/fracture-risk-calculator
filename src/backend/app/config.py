"""
Application configuration and settings
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Configuration
    APP_NAME: str = "BonoAI Fracture Risk API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "ML-powered fracture risk calculator for postmenopausal women"
    )

    # CORS Configuration
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", ["http://localhost:5173"])
    CORS_ORIGIN_REGEX: Optional[str] = os.getenv("CORS_ORIGIN_REGEX", None)

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        case_sensitive = True
        env_file = ".env"


# Create settings instance
settings = Settings()
