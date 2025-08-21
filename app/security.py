from passlib.context import CryptContext
from sqlmodel import Session, select

from app.models.tables import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get the hashed version of a password."""
    return pwd_context.hash(password)


def authenticate_user(session: Session, username: str, password: str) -> bool | User:
    """Authenticate a user by username and password."""
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
