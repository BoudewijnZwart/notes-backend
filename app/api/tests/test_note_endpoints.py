from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.api.routes.notes import NOTES_ROUTE_PREFIX
from app.models.tests.factories import TagFactory
from app.models.tables import Folder, Note


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


@pytest.mark.parametrize("post_body_fixture", ["post_body_with_tags"])
def test_create_note_correct_input(
    post_body_fixture: dict[str, Any],
    request: pytest.FixtureRequest,
    session: Session,
    client: TestClient,
) -> None:
    """Test creating a note."""
    # GIVEN a request body for creating a note
    post_body = request.getfixturevalue(post_body_fixture)

    # AND an empty database
    statement = select(Note.id).limit(1)
    assert session.exec(statement).first() is None

    # WHEN the client sends a POST request to the notes endpoint
    response = client.post(f"{NOTES_ROUTE_PREFIX}/", json=post_body)

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
