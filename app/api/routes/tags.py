from typing import Any

from fastapi import APIRouter, status
from sqlmodel import select

from app.api.deps import SessionDep
from app.api.routes.constants import TAG_ROUTE_PREFIX
from app.api.schemas.tags import TagNew, TagPublic
from app.crud import (
    get_object_or_404_by_owner,
    get_tag_by_parent_and_name,
)
from app.models.tables import Tag
from app.security import CurrentUser

router = APIRouter(prefix=TAG_ROUTE_PREFIX, tags=["tags"])


@router.get("/{tag_id}", response_model=TagPublic)
async def get_tag(tag_id: int, user: CurrentUser, session: SessionDep) -> Tag:
    """Endpoint to get a tag by ID."""
    tag = get_object_or_404_by_owner(Tag, tag_id, user.id, session)
    return TagPublic.from_tag(tag)


@router.get("/", response_model=list[TagPublic])
async def get_all_tags(session: SessionDep) -> Any:
    """Endpoint to get all tags."""
    statement = select(Tag)
    tags = session.exec(statement).all()

    return [TagPublic.from_tag(tag) for tag in tags]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tag(tag_request: TagNew, session: SessionDep) -> None:
    """Endpoint to create a tag."""
    tag_names = Tag.full_name_to_tag_names(tag_request.full_name)

    parent_id = None
    created_tags = []

    for tag_name in tag_names:
        possible_tag = get_tag_by_parent_and_name(parent_id, tag_name, session)
        if possible_tag is None:
            new_tag = Tag(name=tag_name, parent_id=parent_id)
            session.add(new_tag)
            session.commit()
            session.refresh(new_tag)
            parent_id = new_tag.id
            created_tags.append(tag_name)
        else:
            parent_id = possible_tag.id


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, user: CurrentUser, session: SessionDep) -> None:
    """Endpoint to delete a tag by ID."""
    tag = get_object_or_404_by_owner(Tag, tag_id, user.id, session)
    session.delete(tag)
    session.commit()
