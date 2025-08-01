"""All the database tables used in the application."""

from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.basemodels import FolderBase, NoteBase, TagBase
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
        return [part for part in full_name.strip().split("/") if part]
