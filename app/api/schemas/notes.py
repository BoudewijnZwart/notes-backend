from typing import Self

from app.models.basemodels import NoteBase
from app.models.tables import Note


class NotePublic(NoteBase):
    """Schema for a note returned to the public."""

    id: int
    tag_ids: list[int]

    @classmethod
    def from_note(cls, note: Note) -> Self:
        """Create a NotePublic from a Note."""
        if note.id is None:
            msg = "Missing primary key."
            raise ValueError(msg)

        return cls(
            id=note.id,
            title=note.title,
            body=note.body,
            tag_ids=[tag.id for tag in note.tags],
            folder_id=note.folder_id,
        )


class NoteNew(NoteBase):
    """Schema for a new note."""

    folder_id: int | None = None
    tag_ids: list[int]
