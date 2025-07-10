from sqlmodel import Session, select
from fastapi import status, HTTPException

from app.models.notes import Note


def get_note_by_id(session: Session, note_id: int) -> Note | None:
    statement = select(Note).where(Note.id == note_id)
    note = session.exec(statement).first()

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No note found with that id."
        )

    return note
