import uuid
from typing import Any

from fastapi import APIRouter, status
from sqlmodel import select

from app.api.deps import SessionDep
from app.api.schemas.users import UserNew, UserPublic
from app.crud import get_object_or_404
from app.models.tables import User
from app.shared.constants import DEFAULT_LIMIT, DEFAULT_SKIP

USERS_ROUTE_PREFIX = "/users"

router = APIRouter(prefix=USERS_ROUTE_PREFIX, tags=["users"])


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: uuid.UUID, session: SessionDep) -> Any:
    """Endpoint to get a user by id."""
    user = get_object_or_404(User, user_id, session)
    return UserPublic.from_user(user)


@router.get("/", response_model=list[UserPublic])
async def get_users(
    session: SessionDep, skip: int = DEFAULT_SKIP, limit: int = DEFAULT_LIMIT,
) -> Any:
    """Endpoint to get all users."""
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserNew, session: SessionDep):
    """Endpoint to create a new user."""
    user = new_user.into_user()
    session.add(user)
    session.commit()
