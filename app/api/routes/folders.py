from typing import Any

from fastapi import APIRouter, status
from sqlmodel import select

from app.api.deps import SessionDep
from app.api.schemas.folders import FolderNew, FolderPublic
from app.crud import get_object_or_404
from app.models.tables import Folder

FOLDER_ROUTE_PREFIX = "/folders"

router = APIRouter(prefix=FOLDER_ROUTE_PREFIX, tags=["folders"])


@router.get("/{folder_id}", response_model=FolderPublic)
async def get_folder_by_id(folder_id: int, session: SessionDep) -> Any:
    """Endpoint to get a folder by ID."""
    return get_object_or_404(Folder, folder_id, session)


@router.get("/", response_model=list[FolderPublic])
async def get_all_folders(session: SessionDep) -> Any:
    """Endpoint to get all folders."""
    statement = select(Folder)
    return session.exec(statement).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_folder(folder_request: FolderNew, session: SessionDep) -> None:
    """Endpoint to create a folder."""
    new_folder = Folder(**folder_request.model_dump())

    session.add(new_folder)
    session.commit()
