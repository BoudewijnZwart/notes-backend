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


class FolderBase(SQLModel):
    """Base model for a folder."""

    name: str = Field(max_length=128)
