from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.api.routes.users import USERS_ROUTE_PREFIX
from app.models.tables import User
from tests.typedefs import Outcome


@pytest.mark.parametrize(
    ("new_user_data", "expected_outcome"),
    [
        pytest.param(
            {
                "email": "test@gmail.com",
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
