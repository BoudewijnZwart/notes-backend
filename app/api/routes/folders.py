from typing import Any

from fastapi import APIRouter, status

from app.api.deps import SessionDep
from app.api.schemas.folders import FolderNew, FolderPublic
from app.crud import get_object_or_404_by_owner, get_objects_by_owner
from app.models.tables import Folder
from app.security import CurrentUser

FOLDER_ROUTE_PREFIX = "/folders"

router = APIRouter(prefix=FOLDER_ROUTE_PREFIX, tags=["folders"])


@router.get("/{folder_id}", response_model=FolderPublic)
async def get_folder_by_id(
    folder_id: int, user: CurrentUser, session: SessionDep,
) -> Any:
    """Endpoint to get a folder by ID."""
    return get_object_or_404_by_owner(Folder, folder_id, user.id, session)


@router.get("/", response_model=list[FolderPublic])
async def get_all_folders(user: CurrentUser, session: SessionDep) -> Any:
    """Endpoint to get all folders."""
    return get_objects_by_owner(Folder, user.id, session)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_folder(
    folder_request: FolderNew, user: CurrentUser, session: SessionDep,
) -> None:
    """Endpoint to create a folder."""
    folder_data = folder_request.model_dump()
    folder_data["owner_id"] = user.id
    new_folder = Folder(**folder_data)

    session.add(new_folder)
    session.commit()


@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(folder_id: int, user: CurrentUser, session: SessionDep) -> None:
    """Endpoint to delete a folder by ID."""
    folder = get_object_or_404_by_owner(Folder, folder_id, user.id, session)
    session.delete(folder)
    session.commit()
