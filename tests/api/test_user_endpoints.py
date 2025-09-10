from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.api.routes.users import USERS_ROUTE_PREFIX
from app.models.tables import User
from tests.models.factories import UserFactory
from tests.typedefs import Outcome


def test_get_user(user: User, superuser_client: TestClient) -> None:
    """Test get endpoint to get a user by ID."""
    # GIVEN a user in the database

    # AND a client
    client = superuser_client

    # WHEN a get request is made to the endpoint
    response = client.get(f"{USERS_ROUTE_PREFIX}/{user.id}")

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_200_OK

    # AND the response data matches the user data
    response_body = response.json()
    assert response_body["id"] == str(user.id)
    assert response_body["email"] == user.email
    assert response_body["first_name"] == user.first_name
    assert response_body["last_name"] == user.last_name
    assert response_body["is_active"] == user.is_active


def test_get_multiple_users(
    user_factory: type[UserFactory],
    client: TestClient,
) -> None:
    """Test get endpoint to get multiple users."""
    # GIVEN multiple users in the database
    users = user_factory.create_batch(5)

    # WHEN a get request is made to the endpoint
    response = client.get(USERS_ROUTE_PREFIX)

    # THEN the correct status code is returned
    assert response.status_code == status.HTTP_200_OK

    # AND the response data matches the user data
    response_body = response.json()
    assert len(response_body) == len(users)
    for user_data in response_body:
        user = next((u for u in users if str(u.id) == user_data["id"]), None)
        assert user is not None
        assert user_data["email"] == user.email
        assert user_data["first_name"] == user.first_name
        assert user_data["last_name"] == user.last_name
        assert user_data["is_active"] == user.is_active


@pytest.mark.parametrize(
    ("new_user_data", "expected_outcome"),
    [
        pytest.param(
            {
                "email": "test@gmail.com",
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "password": "Testpassword123!",
            },
            Outcome.SUCCESS,
            id="valid user data",
        ),
        pytest.param(
            {
                "email": "test",
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "password": "Testpassword123!",
            },
            Outcome.FAILURE,
            id="invalid email",
        ),
        pytest.param(
            {
                "email": "test@email.com",
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "password": "short",
            },
            Outcome.FAILURE,
            id="invalid password",
        ),
    ],
)
def test_create_user(
    new_user_data: dict[str, Any],
    expected_outcome: Outcome,
    session: Session,
    client: TestClient,
) -> None:
    """Test creating a user using a POST request."""
    # GIVEN some data for creating a new user

    # WHEN a POST request is made to create the user
    response = client.post(f"{USERS_ROUTE_PREFIX}/", json=new_user_data)

    # THEN the correct status code is returned
    match expected_outcome:
        case Outcome.SUCCESS:
            assert response.status_code == status.HTTP_201_CREATED
        case Outcome.FAILURE:
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # AND a user is created in the database with the expected email
    statement = select(User).where(User.email == new_user_data["email"])
    user = session.exec(statement).first()
    match expected_outcome:
        case Outcome.SUCCESS:
            assert user is not None
        case Outcome.FAILURE:
            assert user is None


def test_delete_user(user: User, client: TestClient, session: Session) -> None:
    """Test deleting a user using a DELETE request."""
    # GIVEN a user in the database

    # AND a client

    # WHEN a delete request is sent to the delete endpoint
    response = client.delete(f"{USERS_ROUTE_PREFIX}/{user.id}")

    # THEN the right response code is returned
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # AND the user is removed from the database
    statement = select(User).where(User.id == user.id)
    deleted_user = session.exec(statement).first()
    assert deleted_user is None
