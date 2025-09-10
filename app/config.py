import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.typedefs import EnvironmentType, LOGLevel


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    ENVIRONMENT: EnvironmentType
    DATABASE_URL: str
    LOG_LEVEL: LOGLevel
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()  # type: ignore[call-arg]


def setup_logging(settings: Settings) -> logging.Logger:
    """Set up logging configuration."""
    logger = logging.getLogger(__name__)
    logger.setLevel(settings.LOG_LEVEL.value.upper())
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    return logger


logger = setup_logging(settings)

logger.info("Environment: %s", settings.ENVIRONMENT)
