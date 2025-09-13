from collections.abc import Iterator

import pytest
import pytest_factoryboy
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.api.deps import get_db
from app.main import app
from app.models.tables import User
from tests.models.factories import FolderFactory, NoteFactory, TagFactory, UserFactory
from tests.test_config import engine
from tests.utils import get_auth_header_for_user

# Register factories as fixtures
pytest_factoryboy.register(NoteFactory)
pytest_factoryboy.register(TagFactory)
pytest_factoryboy.register(FolderFactory)
pytest_factoryboy.register(UserFactory)


@pytest.fixture(name="session")
def session_fixture() -> Iterator[Session]:
    """Fixture to provide a session object.

    This fixture will flush the session after each test to ensure a clean state.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session

    session.close()
    transaction.rollback()  # Rollback any changes made during the test
    connection.close()


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Iterator[TestClient]:
    """Fixture to provide a FastAPI test client with a session override."""

    def get_session_override() -> Session:
        """Override the get_db dependency to use the provided session."""
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(user_factory: UserFactory) -> User:
    """Fixture to provide a test user."""
    return user_factory.create()


@pytest.fixture(name="superuser")
def superuser_fixture(user_factory: UserFactory) -> User:
    """Fixture to provide a superuser."""
    return user_factory.create(is_superuser=True)


@pytest.fixture(name="user_client")
def user_client_fixture(client: TestClient, test_user: User) -> Iterator[TestClient]:
    """Fixture to provide a FastAPI test client with a logged-in user."""
    headers = get_auth_header_for_user(test_user.id)
    client.headers.update(headers)
    return client


@pytest.fixture(name="superuser_client")
def superuser_client_fixture(
    client: TestClient,
    superuser: User,
) -> Iterator[TestClient]:
    """Fixture to provide a FastAPI test client with a logged-in superuser."""
    headers = get_auth_header_for_user(superuser.id)
    client.headers.update(headers)
    return client
