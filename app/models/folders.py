from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class FolderBase(SQLModel):
    name: str = Field(max_length=128)


class Folder(FolderBase, table=True):
    id: int | None = Field(primary_key=True, default=None)
    parent_id: int | None = Field(foreign_key="folder.id", default=None)
    parent: Optional["Folder"] = Relationship(
        back_populates="child_folders",
        sa_relationship_kwargs={"remote_side": "Folder.id"},
    )
    child_folders: list["Folder"] = Relationship(back_populates="parent")


class FolderNew(FolderBase):
    parent_id: int | None = Field(default=None)


class FolderPublic(FolderBase):
    id: int
    parent_id: int | None
