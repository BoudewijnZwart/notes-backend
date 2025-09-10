import uuid

from fastapi import HTTPException, status
from sqlmodel import Session, SQLModel, select

from app.models.tables import Tag


def get_object_or_404[T = SQLModel](
    obj_type: type[T],
    obj_id: int,
    session: Session,
) -> T:
    """Get an object by primary key if it exists."""
    if (obj := session.get(obj_type, obj_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nothing found with that id.",
        )

    return obj


def get_object_or_404_by_owner[T = SQLModel](
    obj_type: type[T],
    obj_id: int,
    owner_id: uuid.UUID,
    session: Session,
) -> T:
    """Get an object by primary key and owner id if it exists."""
    statement = select(obj_type).where(
        obj_type.id == obj_id,
        obj_type.owner_id == owner_id,
    )
    if (obj := session.exec(statement).first()) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nothing found with that id.",
        )

    return obj


def get_objects_by_owner[T = SQLModel](
    obj_type: type[T],
    owner_id: uuid.UUID,
    session: Session,
) -> list[T]:
    """Get all objects owned by a specific user."""
    statement = select(obj_type).where(obj_type.owner_id == owner_id)
    return session.exec(statement).all()


def get_tag_by_parent_and_name(
    parent_id: int | None,
    name: str,
    session: Session,
) -> Tag | None:
    """Search for a tag with a specific parent."""
    statement = select(Tag).where(Tag.parent_id == parent_id, Tag.name == name)
    return session.exec(statement).first()
