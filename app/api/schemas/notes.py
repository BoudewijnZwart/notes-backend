from app.models.basemodels import NoteBase


class NotePublic(NoteBase):
    """Schema for a note returned to the public."""

    id: int
    tag_ids: list[int]


class NoteNew(NoteBase):
    """Schema for a new note."""

    folder_id: int | None = None
    tag_ids: list[int]
