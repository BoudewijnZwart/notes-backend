"""All the database tables used in the application."""

import uuid
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.basemodels import FolderBase, NoteBase, TagBase, UserBase
from app.shared.constants import MAX_NAME_LEN, MIN_NAME_LEN


class NoteTagLink(SQLModel, table=True):  # type: ignore[call-arg]
    """Link between a note and a tag."""

    note_id: int | None = Field(foreign_key="note.id", primary_key=True)
    tag_id: int | None = Field(foreign_key="tag.id", primary_key=True)


class Note(NoteBase, table=True):  # type: ignore[call-arg]
    """Representation of a note."""

    id: int | None = Field(primary_key=True, default=None)
    tags: list["Tag"] = Relationship(
        back_populates="notes",
        link_model=NoteTagLink,
    )
    owner_id: uuid.UUID | None = Field(foreign_key="user.id")


class Folder(FolderBase, table=True):  # type: ignore[call-arg]
    """Representation of a folder to group notes."""

    id: int | None = Field(primary_key=True, default=None)
    parent_id: int | None = Field(foreign_key="folder.id", default=None)
    parent: Optional["Folder"] = Relationship(
        back_populates="child_folders",
        sa_relationship_kwargs={"remote_side": "Folder.id"},
    )
    child_folders: list["Folder"] = Relationship(back_populates="parent")


class Tag(TagBase, table=True):  # type: ignore[call-arg]
    """Represents a tag used to group notes."""

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(min_length=MIN_NAME_LEN, max_length=MAX_NAME_LEN)
    parent_id: int | None = Field(foreign_key="tag.id", default=None)
    parent_tag: Optional["Tag"] = Relationship(
        back_populates="child_tags",
        sa_relationship_kwargs={"remote_side": "Tag.id"},
    )
    child_tags: list["Tag"] = Relationship(back_populates="parent_tag")
    notes: list["Note"] = Relationship(
        back_populates="tags",
        link_model=NoteTagLink,
    )

    def get_full_name(self) -> str:
        """Get the full name of a tag."""
        full_name = self.name
        if self.parent_tag is not None:
            full_name = self.parent_tag.get_full_name() + "/" + full_name
        return full_name

    @staticmethod
    def full_name_to_tag_names(full_name: str) -> list[str]:
        """Split a given full tag name into separate tag names."""
        seperate_names = [part for part in full_name.strip().split("/") if part]
        return [Tag.clean_tag_name(name) for name in seperate_names]

    @staticmethod
    def clean_tag_name(tag_name: str) -> str:
        """Clean a tag name."""
        return tag_name.strip().lower()


class User(UserBase, table=True):  # type: ignore[call-arg]
    """Represents a user."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
