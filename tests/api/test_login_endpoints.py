from fastapi import status
from fastapi.testclient import TestClient

from app.api.routes.constants import LOGIN_ROUTE_PREFIX
from tests.constants import TEST_USER_PASSWORD
from tests.models.factories import UserFactory


def test_create_access_token(user_factory: UserFactory, client: TestClient) -> None:
    """Test creating an access token using the token endpoint."""
    # GIVEN a user with a known password
    user_factory.create(username="testuser", password=TEST_USER_PASSWORD)

    # WHEN they provide their credentials to the login endpoint
    response = client.post(
        f"{LOGIN_ROUTE_PREFIX}/token",
        data={"username": "testuser", "password": TEST_USER_PASSWORD},
    )

    # THEN they receive a token
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"  # noqa: S105
