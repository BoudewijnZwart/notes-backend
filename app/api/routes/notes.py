from typing import Annotated, Any

from fastapi import APIRouter, Path, status
from sqlmodel import select

from app.api.deps import SessionDep
from app.crud import get_object_or_404
from app.models.notes import Note, NoteNew, NotePublic

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/{note_id}", response_model=NotePublic)
async def get_note(note_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Any:
    """Endpoint to get a note by id."""
    return get_object_or_404(Note, note_id, session)


@router.get("/", response_model=list[NotePublic])
async def get_all_notes(session: SessionDep) -> Any:
    """Endpoint to get all notes."""
    statement = select(Note)
    return session.exec(statement).all()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_note(session: SessionDep, note_request: NoteNew) -> Any:
    """Endpoint to create a new note."""
    note = Note(**note_request.model_dump())

    session.add(note)
    session.commit()


@router.put("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_note(
    session: SessionDep,
    note_request: NoteNew,
    note_id: Annotated[int, Path(gt=0)],
) -> None:
    """Endpoint to update a note."""
    note = get_object_or_404(Note, note_id, session)

    note.title = note_request.title
    note.body = note_request.body

    session.add(note)
    session.commit()


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(session: SessionDep, note_id: Annotated[int, Path(gt=0)]) -> None:
    """Endpoint to delete a note."""
    note = get_object_or_404(Note, note_id, session)

    session.delete(note)
    session.commit()
