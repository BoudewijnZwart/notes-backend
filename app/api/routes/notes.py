from typing import Annotated, Any

from fastapi import APIRouter, Path, status
from sqlmodel import select

from app.api.deps import SessionDep
from app.api.schemas.notes import NoteNew, NotePublic
from app.crud import get_object_or_404
from app.models.tables import Note, Tag

NOTES_ROUTE_PREFIX = "/notes"

router = APIRouter(prefix=NOTES_ROUTE_PREFIX, tags=["notes"])


@router.get("/{note_id}", response_model=NotePublic)
async def get_note(note_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Any:
    """Endpoint to get a note by id."""
    return get_object_or_404(Note, note_id, session)


@router.get("/", response_model=list[NotePublic])
async def get_all_notes(session: SessionDep) -> Any:
    """Endpoint to get all notes."""
    statement = select(Note)
    notes = session.exec(statement).all()
    return [NotePublic.from_note(note) for note in notes]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_note(session: SessionDep, note_request: NoteNew) -> Any:
    """Endpoint to create a new note."""
    post_body = note_request.model_dump()

    # If the request contains tag ids, fetch the tags from the database
    if len(tag_ids := post_body.pop("tag_ids", [])) > 0:
        post_body["tags"] = [session.get(Tag, tag_id) for tag_id in tag_ids]

    note = Note(**post_body)

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
