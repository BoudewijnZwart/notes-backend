from typing import Any

from fastapi import APIRouter
from sqlmodel import select

from app.api.deps import SessionDep
from app.models.tags import Tag, TagNew, TagPublic


router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=list[TagPublic])
async def get_all_tags(session: SessionDep) -> Any:
    """Endpoint to get all tags."""

    statement = select(Tag)
    tags: list[Tag] = session.exec(statement).all()

    return [
        TagPublic(
            id=tag.id,
            name=tag.name,
            full_name=tag.get_full_name(),
            parent_id=tag.parent_id,
            child_ids=[child.id for child in tag.child_tags],
        )
        for tag in tags
    ]


@router.post("/")
async def create_tag(tag_request: TagNew, session: SessionDep) -> None:
    """Endpoint to create a tag."""

    new_tag = Tag(name=tag_request.full_name)

    session.add(new_tag)
    session.commit()
