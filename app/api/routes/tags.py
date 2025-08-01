from typing import Any

from fastapi import APIRouter
from sqlmodel import select

from app.api.deps import SessionDep
from app.api.schemas.tags import TagNew, TagPublic
from app.crud import get_tag_by_parent_and_name
from app.models.tables import Tag

TAG_ROUTE_PREFIX = "/tags"

router = APIRouter(prefix=TAG_ROUTE_PREFIX, tags=["tags"])


@router.get("/", response_model=list[TagPublic])
async def get_all_tags(session: SessionDep) -> Any:
    """Endpoint to get all tags."""
    statement = select(Tag)
    tags = session.exec(statement).all()

    return [TagPublic.from_tag(tag) for tag in tags]


@router.post("/")
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
