from enum import StrEnum


class EnvironmentType(StrEnum):
    """Enumeration for different environment types."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LOGLevel(StrEnum):
    """Enumeration for log levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
