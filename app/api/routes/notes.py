from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Path, status
from sqlmodel import select

from app.api.deps import SessionDep
from app.api.routes.constants import NOTES_ROUTE_PREFIX
from app.api.schemas.notes import NoteNew, NotePublic
from app.crud import get_object_or_404
from app.models.tables import Note, Tag
from app.security import CurrentUser

router = APIRouter(prefix=NOTES_ROUTE_PREFIX, tags=["notes"])


@router.get("/{note_id}", response_model=NotePublic)
async def get_note(
    note_id: Annotated[int, Path(gt=0)],
    session: SessionDep,
    user: CurrentUser,
) -> Any:
    """Endpoint to get a note by id.

    If the note does not belong to the current user, a 404 error is raised.
    """
    note = get_object_or_404(Note, note_id, session)

    if note.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Note not found")

    return NotePublic.from_note(note)


@router.get("/", response_model=list[NotePublic])
async def get_all_notes(user: CurrentUser, session: SessionDep) -> Any:
    """Endpoint to get all notes for a specific owner."""
    statement = select(Note).where(Note.owner_id == user.id)
    notes = session.exec(statement).all()
    return [NotePublic.from_note(note) for note in notes]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_note(
    user: CurrentUser,
    note_request: NoteNew,
    session: SessionDep,
) -> Any:
    """Endpoint to create a new note."""
    post_body = note_request.model_dump()

    # If the request contains tag ids, fetch the tags from the database
    if len(tag_ids := post_body.pop("tag_ids", [])) > 0:
        post_body["tags"] = [session.get(Tag, tag_id) for tag_id in tag_ids]

    # Add the owner id to the note
    post_body["owner_id"] = user.id

    note = Note(**post_body)

    session.add(note)
    session.commit()


@router.put("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_note(
    user: CurrentUser,
    note_request: NoteNew,
    note_id: Annotated[int, Path(gt=0)],
    session: SessionDep,
) -> None:
    """Endpoint to update a note."""
    note = get_object_or_404(Note, note_id, session)

    if note.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = note_request.title
    note.body = note_request.body
    note.folder_id = note_request.folder_id
    note.tags = [session.get(Tag, tag_id) for tag_id in note_request.tag_ids]

    session.add(note)
    session.commit()


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    user: CurrentUser,
    session: SessionDep,
    note_id: Annotated[int, Path(gt=0)],
) -> None:
    """Endpoint to delete a note."""
    note = get_object_or_404(Note, note_id, session)

    if note.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Note not found")

    session.delete(note)
    session.commit()
