from pydantic import BaseModel, Field

from app.shared.constants import (
    MAX_NOTE_BODY_LEN,
    MIN_NOTE_TITLE_LEN,
    MAX_NOTE_TITLE_LEN,
)


class NoteBase(BaseModel):
    title: str = Field(min_length=MIN_NOTE_TITLE_LEN, max_length=MAX_NOTE_TITLE_LEN)
    body: str = Field(max_length=MAX_NOTE_BODY_LEN)
    private: bool


class NoteNew(NoteBase):
    pass


class NoteResponse(NoteBase):
    id: int


class NotesResponse(BaseModel):
    data: list[NoteResponse]
    count: int
