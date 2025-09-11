from sqlmodel import Session, select

from app.config import settings
from app.database import create_db_and_tables, engine
from app.models.tables import User
from app.security import get_password_hash


def create_first_superuser(session: Session) -> None:
    """Create the first superuser."""
    statement = select(User).where(User.username == settings.FIRST_SUPERUSER_USERNAME)
    user = session.exec(statement).first()
    if not user:
        user = User(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        )
        session.add(user)
        session.commit()


def startup() -> None:
    """Startup tasks to run when the application starts."""
    create_db_and_tables()

    with Session(engine) as session:
        create_first_superuser(session)
