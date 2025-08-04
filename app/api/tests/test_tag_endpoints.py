import pytest

from app.api.routes.tags import TAG_ROUTE_PREFIX
from app.models.tables import Tag
from fastapi import status
from fastapi.testclient import TestClient
from app.models.tests.factories import TagFactory
from sqlmodel import Session, select

from pytest import param

def test_get_tag_by_id(
    tag: Tag,
    client: TestClient,
) -> None:
    """Test retrieving a tag by ID."""
    # GIVEN a tag in the database

    # WHEN the client sends a GET request to the tags endpoint with the tag ID
    response = client.get(f"{TAG_ROUTE_PREFIX}/{tag.id}")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_200_OK

    # AND the response contains the correct data
    response_data = response.json()
    assert response_data["id"] == tag.id
    assert response_data["name"] == tag.name

def get_all_tags(
    tag_factory: TagFactory,
    client: TestClient,
) -> None:
    """Test retrieving all tags in the database."""
    # GIVEN multiple tags in the database
    tags = tag_factory.create_batch(3)

    # WHEN the client sends a GET request to the tags endpoint
    response = client.get(f"{TAG_ROUTE_PREFIX}/")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_200_OK

    # AND the response contains all the tags
    response_data = response.json()
    assert len(response_data) == len(tags)
    for tag, response_tag in zip(tags, response_data):
        assert response_tag["id"] == tag.id
        assert response_tag["name"] == tag.name


@pytest.fixture(name="existing_tag")
def existing_tag_fixture(tag_factory: TagFactory) -> Tag:
    """Fixture to create an existing tag."""
    return tag_factory.create(name="Existing Tag")

@pytest.mark.parametrize(("post_body", "expected_tag_names"),[
    param({"full_name": "Tag_1"}, ["tag_1"], id="simple root tag"),
    param({"full_name": "Tag 2"}, ["tag 2"], id="simple root tag with space"),
    param({"full_name": "root_tag/child_tag/2nd_child_tag"}, ["root_tag", "child_tag", "2nd_child_tag"], id="multiple tags that do not exist yet"),
    param({"full_name": "existing_tag/child_tag"}, ["existing_tag", "child_tag"], id="existing tag with child tag"),
])
def test_create_tag(
    post_body: dict[str, str],
    expected_tag_names: list[str],
    client: TestClient,
    session: Session,
) -> None:
    """Test creating a new tag."""
    # GIVEN a request body for creating a tag

    # AND a client to send requests

    # WHEN the client sends a POST request to the tags endpoint
    response = client.post(f"{TAG_ROUTE_PREFIX}/", json=post_body)

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_201_CREATED

    # AND the correct tags are created in the database
    created_tags = session.exec(select(Tag)).all()
    created_tag_names = [tag.name for tag in created_tags]
    assert set(created_tag_names) == set(expected_tag_names)
    

def test_delete_tag(
    existing_tag: Tag,
    client: TestClient,
    session: Session,
) -> None:
    """Test deleting a tag by ID."""
    # GIVEN an existing tag in the database

    # WHEN the client sends a DELETE request to the tags endpoint with the tag ID
    response = client.delete(f"{TAG_ROUTE_PREFIX}/{existing_tag.id}")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # AND the tag is removed from the database
    deleted_tag = session.get(Tag, existing_tag.id)
    assert deleted_tag is None