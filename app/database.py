from sqlmodel import SQLModel, create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    """Create all tables if they do not exist yet."""
    SQLModel.metadata.create_all(engine)
