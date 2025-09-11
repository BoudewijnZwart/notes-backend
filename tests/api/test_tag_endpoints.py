import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.api.routes.constants import TAG_ROUTE_PREFIX
from app.models.tables import Tag, User
from tests.models.factories import TagFactory


def test_get_tag_by_id(
    tag_factory: TagFactory,
    test_user: User,
    user_client: TestClient,
) -> None:
    """Test retrieving a tag by ID."""
    # GIVEN a tag in the database owned by the test user
    tag = tag_factory.create(owner_id=test_user.id)

    # WHEN the client sends a GET request to the tags endpoint with the tag ID
    response = user_client.get(f"{TAG_ROUTE_PREFIX}/{tag.id}")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_200_OK

    # AND the response contains the correct data
    response_data = response.json()
    assert response_data["id"] == tag.id
    assert response_data["name"] == tag.name


def test_get_all_tags(
    tag_factory: TagFactory,
    test_user: User,
    user_client: TestClient,
) -> None:
    """Test retrieving all tags in the database."""
    # GIVEN multiple tags in the database
    tags = tag_factory.create_batch(3, owner_id=test_user.id)

    # WHEN the client sends a GET request to the tags endpoint
    response = user_client.get(f"{TAG_ROUTE_PREFIX}/")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_200_OK

    # AND the response contains all the tags
    response_data = response.json()
    assert len(response_data) == len(tags)
    for tag, response_tag in zip(tags, response_data, strict=False):
        assert response_tag["id"] == tag.id
        assert response_tag["name"] == tag.name


@pytest.fixture(name="existing_tag")
def existing_tag_fixture(tag_factory: TagFactory, test_user: User) -> Tag:
    """Fixture to create an existing tag."""
    return tag_factory.create(name="Existing Tag", owner_id=test_user.id)


@pytest.mark.parametrize(
    ("post_body", "expected_tag_names"),
    [
        pytest.param({"full_name": "Tag_1"}, ["tag_1"], id="simple root tag"),
        pytest.param(
            {"full_name": "Tag 2"},
            ["tag 2"],
            id="simple root tag with space",
        ),
        pytest.param(
            {"full_name": "root_tag/child_tag/2nd_child_tag"},
            ["root_tag", "child_tag", "2nd_child_tag"],
            id="multiple tags that do not exist yet",
        ),
        pytest.param(
            {"full_name": "existing_tag/child_tag"},
            ["existing_tag", "child_tag"],
            id="existing tag with child tag",
        ),
    ],
)
def test_create_tag(
    post_body: dict[str, str],
    expected_tag_names: list[str],
    test_user: User,
    user_client: TestClient,
    session: Session,
) -> None:
    """Test creating a new tag."""
    # GIVEN a request body for creating a tag with the owner id
    post_body["owner_id"] = str(test_user.id)

    # AND a client to send requests
    client = user_client

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
    user_client: TestClient,
    session: Session,
) -> None:
    """Test deleting a tag by ID."""
    # GIVEN an existing tag in the database

    # WHEN the client sends a DELETE request to the tags endpoint with the tag ID
    response = user_client.delete(f"{TAG_ROUTE_PREFIX}/{existing_tag.id}")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # AND the tag is removed from the database
    deleted_tag = session.get(Tag, existing_tag.id)
    assert deleted_tag is None
