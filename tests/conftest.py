from collections.abc import Iterator

import pytest
import pytest_factoryboy
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.api.deps import get_db
from app.main import app
from tests.models.factories import FolderFactory, NoteFactory, TagFactory, UserFactory
from tests.test_config import engine

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
