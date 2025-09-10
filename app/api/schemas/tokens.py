from sqlmodel import SQLModel


class Token(SQLModel):
    """Schema for JWT token."""

    access_token: str
    token_type: str = "bearer"  # noqa: S105


class TokenPayload(SQLModel):
    """Payload for JWT token."""

    sub: str | None = None
