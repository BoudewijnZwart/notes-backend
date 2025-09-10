import uuid
from typing import Any

from fastapi import APIRouter, status
from sqlmodel import select

from app.api.deps import SessionDep
from app.api.schemas.users import UserNew, UserPublic
from app.crud import get_object_or_404
from app.models.tables import User
from app.security import CurrentActiveSuperUser
from app.shared.constants import DEFAULT_LIMIT, DEFAULT_SKIP

USERS_ROUTE_PREFIX = "/users"

router = APIRouter(prefix=USERS_ROUTE_PREFIX, tags=["users"])


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(
    user_id: uuid.UUID,
    superuser: CurrentActiveSuperUser,
    session: SessionDep,
) -> Any:
    """Endpoint to get a user by id."""
    del superuser  # Unused, but ensures only superusers can access this endpoint
    user = get_object_or_404(User, user_id, session)
    return UserPublic.from_user(user)


@router.get("/", response_model=list[UserPublic])
async def get_users(
    superuser: CurrentActiveSuperUser,
    session: SessionDep,
    skip: int = DEFAULT_SKIP,
    limit: int = DEFAULT_LIMIT,
) -> Any:
    """Endpoint to get all users."""
    del superuser  # Unused, but ensures only superusers can access this endpoint
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: UserNew,
    superuser: CurrentActiveSuperUser,
    session: SessionDep,
) -> None:
    """Endpoint to create a new user."""
    del superuser  # Unused, but ensures only superusers can access this endpoint
    user = new_user.into_user()
    session.add(user)
    session.commit()


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    superuser: CurrentActiveSuperUser,
    session: SessionDep,
) -> None:
    """Endpoint to delete a user."""
    del superuser  # Unused, but ensures only superusers can access this endpoint
    user = get_object_or_404(User, user_id, session)

    session.delete(user)
    session.commit()
