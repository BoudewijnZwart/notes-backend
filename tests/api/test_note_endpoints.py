from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.api.routes.constants import NOTES_ROUTE_PREFIX
from app.models.tables import Folder, Note, User
from tests.models.factories import NoteFactory, TagFactory


@pytest.fixture(name="post_body_simple")
def post_body_simple_fixture() -> dict[str, Any]:
    return {"title": "Test Note", "body": "This is a test note.", "tag_ids": []}


@pytest.fixture(name="post_body_with_folder")
def post_body_with_folder_fixture(folder: Folder) -> dict[str, Any]:
    return {
        "title": "Test Note",
        "body": "This is a test note.",
        "tag_ids": [],
        "folder_id": folder.id,
    }


@pytest.fixture(name="post_body_with_tags")
def post_body_with_tags_fixture(tag_factory: TagFactory) -> dict[str, Any]:
    tag1, tag2 = tag_factory.create_batch(2)
    return {
        "title": "Test Note",
        "body": "This is a test note.",
        "tag_ids": [tag1.id, tag2.id],
    }


@pytest.mark.parametrize(
    "post_body_fixture",
    ["post_body_simple", "post_body_with_folder", "post_body_with_tags"],
)
def test_create_note_correct_input(
    post_body_fixture: dict[str, Any],
    request: pytest.FixtureRequest,
    session: Session,
    user_client: TestClient,
) -> None:
    """Test creating a note."""
    # GIVEN a request body for creating a note
    post_body = request.getfixturevalue(post_body_fixture)

    # AND an empty database
    statement = select(Note.id).limit(1)
    assert session.exec(statement).first() is None

    # WHEN the client sends a POST request to the notes endpoint
    response = user_client.post(f"{NOTES_ROUTE_PREFIX}/", json=post_body)

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_201_CREATED

    # AND the response contains the supplied data
    statement = select(Note)
    created_note = session.exec(statement).first()
    assert created_note.title == post_body["title"]
    assert created_note.body == post_body["body"]
    assert [t.id for t in created_note.tags] == post_body["tag_ids"]
    if (folder_id_post_body := post_body.get("folder_id", None)) is not None:
        assert folder_id_post_body == post_body.get("folder_id", None)


def test_get_note_by_id(
    note_factory: NoteFactory,
    user_client: TestClient,
    test_user: User,
) -> None:
    """Test retrieving a note by ID."""
    # GIVEN a note in the database
    note = note_factory.create(owner_id=test_user.id)

    # WHEN the client sends a GET request to the notes endpoint with the note ID
    response = user_client.get(f"{NOTES_ROUTE_PREFIX}/{note.id}")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_200_OK

    # AND the response contains the correct data
    response_data = response.json()
    assert response_data["id"] == note.id
    assert response_data["title"] == note.title
    assert response_data["body"] == note.body


def test_get_all_notes(
    note_factory: NoteFactory,
    test_user: User,
    user_client: TestClient,
) -> None:
    """Test retrieving all notes in the database."""
    # GIVEN multiple notes in the database
    notes = note_factory.create_batch(3, owner_id=test_user.id)

    # WHEN the client sends a GET request to the notes endpoint with the note ID
    response = user_client.get(f"{NOTES_ROUTE_PREFIX}/")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_200_OK

    # AND the response contains all the notes
    response_data = response.json()
    assert len(response_data) == len(notes)


def test_update_note(
    note_factory: NoteFactory,
    post_body_simple: dict[str, Any],
    user_client: TestClient,
    test_user: User,
    session: Session,
) -> None:
    """Test updating a note."""
    # GIVEN a note in the database
    note = note_factory.create(owner_id=test_user.id)

    # WHEN the client sends a PUT request to the notes endpoint with the note ID
    response = user_client.put(f"{NOTES_ROUTE_PREFIX}/{note.id}", json=post_body_simple)

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # AND the note is updated in the database
    updated_note = session.get(Note, note.id)
    assert updated_note.title == post_body_simple["title"]
    assert updated_note.body == post_body_simple["body"]


def test_delete_note(
    note_factory: NoteFactory,
    user_client: TestClient,
    test_user: User,
    session: Session,
) -> None:
    """Test deleting a note."""
    # GIVEN a note in the database
    note = note_factory.create(owner_id=test_user.id)

    # WHEN the client sends a DELETE request to the notes endpoint with the note ID
    response = user_client.delete(f"{NOTES_ROUTE_PREFIX}/{note.id}")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # AND the note is deleted from the database
    deleted_note = session.get(Note, note.id)
    assert deleted_note is None
