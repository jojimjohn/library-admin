"""Configuration module for PTC Library Admin Dashboard."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""

    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "library_bot")
    DB_USER = os.getenv("DB_USER", "libraryuser")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    # Evolution API
    EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "https://api.ptcau.com")
    EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
    EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "ptc")

    # App
    APP_PORT = int(os.getenv("APP_PORT", "3000"))
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")

    # Admin Auth
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme123")

    # Timezone
    TIMEZONE = os.getenv("TIMEZONE", "Australia/Perth")

    @classmethod
    def get_db_connection_string(cls):
        """Get PostgreSQL connection string."""
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.DB_PASSWORD:
            raise ValueError("DB_PASSWORD must be set")
        return True
