from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from app.models.notes import Note


def get_note_by_id(session: Session, note_id: int) -> Note | None:
    note = session.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No note found with that id."
        )

    return note
