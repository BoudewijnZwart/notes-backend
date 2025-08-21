import uuid

from sqlmodel import Field

from app.models.basemodels import UserBase
from app.models.tables import User
from app.security import get_password_hash
from app.shared.constants import MAX_PASSWORD_LEN, MIN_PASSWORD_LEN


class UserNew(UserBase):
    """Schema for a new user."""

    password: str = Field(min_length=MIN_PASSWORD_LEN, max_length=MAX_PASSWORD_LEN)

    def into_user(self) -> User:
        """Create a User from a NewUser object."""
        return User(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            hashed_password=get_password_hash(self.password),
            is_active=True,
        )


class UserPublic(UserBase):
    """Schema for a public user."""

    id: uuid.UUID
    hashed_password: str
