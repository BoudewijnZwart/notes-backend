from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.api.routes.constants import FOLDER_ROUTE_PREFIX
from app.models.tables import Folder, User
from tests.models.factories import FolderFactory


def test_get_folder_by_id(
    folder_factory: FolderFactory,
    test_user: User,
    user_client: TestClient,
) -> None:
    """Test retrieving a folder by ID."""
    # GIVEN a folder in the database owned by the test user
    folder = folder_factory.create(owner_id=test_user.id)

    # WHEN the client sends a GET request to the folders endpoint with the folder ID
    response = user_client.get(f"{FOLDER_ROUTE_PREFIX}/{folder.id}")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_200_OK

    # AND the response contains the correct data
    response_data = response.json()
    assert response_data["id"] == folder.id
    assert response_data["name"] == folder.name


def test_get_all_folders(
    folder_factory: FolderFactory,
    test_user: User,
    user_client: TestClient,
) -> None:
    """Test retrieving all folders in the database."""
    # GIVEN multiple folders in the database
    folders = folder_factory.create_batch(3, owner_id=test_user.id)

    # WHEN the client sends a GET request to the folders endpoint
    response = user_client.get(f"{FOLDER_ROUTE_PREFIX}/")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_200_OK

    # AND the response contains all the folders
    response_data = response.json()
    assert len(response_data) == len(folders)
    for folder, response_folder in zip(folders, response_data, strict=False):
        assert response_folder["id"] == folder.id
        assert response_folder["name"] == folder.name


@pytest.fixture(name="root_level_folder_data")
def root_level_folder_data_fixture() -> dict[str, Any]:
    """Fixture to create data for a root level folder."""
    return {"name": "Root Folder"}


@pytest.fixture(name="nested_folder_data")
def nested_folder_data_fixture(folder: Folder) -> dict[str, Any]:
    """Fixture to create data for a nested folder."""
    return {"name": "A nested folder", "parent_id": folder.id}


@pytest.mark.parametrize(
    "post_body_fixture",
    [
        "root_level_folder_data",
        "nested_folder_data",
    ],
)
def test_create_folder(
    post_body_fixture: str,
    request: pytest.FixtureRequest,
    session: Session,
    test_user: User,
    user_client: TestClient,
) -> None:
    """Test creating a folder."""
    # GIVEN a post body for creating a folder
    post_body = request.getfixturevalue(post_body_fixture)
    post_body["owner_id"] = str(test_user.id)

    # WHEN the client sends a POST request to the folders endpoint
    response = user_client.post(f"{FOLDER_ROUTE_PREFIX}/", json=post_body)

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_201_CREATED

    # AND a folder is created in the database with the expected name
    statement = select(Folder).where(Folder.name == post_body["name"])
    folder = session.exec(statement).first()
    assert folder is not None

    if "parent_id" in post_body:
        assert folder.parent_id == post_body["parent_id"]


def test_delete_folder(
    folder_factory: FolderFactory,
    test_user: User,
    user_client: TestClient,
    session: Session,
) -> None:
    """Test deleting a folder."""
    # GIVEN an existing folder in the database
    folder = folder_factory.create(owner_id=test_user.id)

    # WHEN the client sends a DELETE request to the folders endpoint with the folder ID
    response = user_client.delete(f"{FOLDER_ROUTE_PREFIX}/{folder.id}")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # AND the note is deleted from the database
    deleted_folder = session.get(Folder, folder.id)
    assert deleted_folder is None
