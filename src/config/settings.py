import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from src.utils.logger import logger

class Settings(BaseSettings):
    """Application settings and configuration"""
    GOOGLE_API_KEY: str
    DATABASE_URI: str = "sqlite:///data_base/northwind.db"
    MODEL_NAME: str = "gemini-1.5-flash-latest"
    TEMPERATURE: float = 0.0
    DEBUG: bool = False
    INCLUDE_TABLES: list[str] | None = None
    SAMPLE_ROWS: int = 3
    LANGCHAIN_API_KEY: str
    LANGCHAIN_TRACING_V2: bool

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    logger.info("Loading application settings")
    try:
        settings = Settings()
        logger.info("Settings loaded successfully")
        # Log configuration details (excluding sensitive information)
        logger.info(f"Database URI configured: {'Yes' if settings.DATABASE_URI else 'No'}")
        logger.info(f"Model name: {settings.MODEL_NAME}")
        logger.info(f"LangChain tracing enabled: {settings.LANGCHAIN_TRACING_V2}")
        return settings
    except Exception as e:
        logger.error(f"Error loading settings: {str(e)}", exc_info=True)
        raise