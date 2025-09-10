import uuid

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class NoteBase(SQLModel):
    """Base model for a note."""

    title: str = Field()
    body: str = Field()
    folder_id: int | None = Field(
        foreign_key="folder.id",
        default=None,
        ondelete="CASCADE",
    )


class TagBase(SQLModel):
    """Base model for a tag."""

    owner_id: uuid.UUID | None = Field(foreign_key="user.id")


class FolderBase(SQLModel):
    """Base model for a folder."""

    name: str = Field(max_length=128)
    owner_id: uuid.UUID | None = Field(foreign_key="user.id")


class UserBase(SQLModel):
    """Base model for a user."""

    username: str = Field(unique=True, index=True, max_length=255)
    email: EmailStr = Field(index=True, max_length=255)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
