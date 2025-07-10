from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class FolderBase(SQLModel):
    """Base model for a folder."""

    name: str = Field(max_length=128)


class Folder(FolderBase, table=True):
    """Representation of a folder to group notes."""

    id: int | None = Field(primary_key=True, default=None)
    parent_id: int | None = Field(foreign_key="folder.id", default=None)
    parent: Optional["Folder"] = Relationship(
        back_populates="child_folders",
        sa_relationship_kwargs={"remote_side": "Folder.id"},
    )
    child_folders: list["Folder"] = Relationship(back_populates="parent")


class FolderNew(FolderBase):
    """Schema for a new folder."""

    parent_id: int | None = Field(default=None)


class FolderPublic(FolderBase):
    """Schema for a folder returned to the public."""

    id: int
    parent_id: int | None
