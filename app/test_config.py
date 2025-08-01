from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool

# global engine for unit tests, using an in-memory SQLite database for testing purposes
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SQLModel.metadata.create_all(engine)
