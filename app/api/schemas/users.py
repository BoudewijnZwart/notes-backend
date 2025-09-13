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
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            hashed_password=get_password_hash(self.password),
            is_active=True,
        )


class UserPublic(UserBase):
    """Schema for a public user."""

    id: uuid.UUID
    is_active: bool

    @classmethod
    def from_user(cls, user: User) -> "UserPublic":
        """Create a UserPublic from a User object."""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
        )
