from sqlmodel import Field, SQLModel


class NoteBase(SQLModel):
    """Base model for a note."""

    title: str = Field()
    body: str = Field()
    folder: int | None = Field(
        foreign_key="folder.id",
        default=None,
        ondelete="CASCADE",
    )


class Note(NoteBase, table=True):
    """Representation of a note."""

    id: int | None = Field(primary_key=True, default=None)


class NotePublic(NoteBase):
    """Schema for a note returned to the public."""

    id: int


class NoteNew(NoteBase):
    """Schema for a new note."""
