
from fastapi import HTTPException, status
from sqlmodel import Session, SQLModel


def get_object_or_404[T = SQLModel](
    obj_type: type[T], obj_id: int, session: Session,
) -> T:
    """Get an object by primary key if it exists."""
    if (obj := session.get(obj_type, obj_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nothing found with that id.",
        )

    return obj
