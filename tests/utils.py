from datetime import timedelta

from app.security import create_access_token


def get_auth_header_for_user(
    user_id: int,
    headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Generate an authorization header for a given user ID."""
    if headers is None:
        headers = {}
    token = create_access_token(
        subject=str(user_id),
        expires_delta=timedelta(minutes=30),
    )
    headers["Authorization"] = f"Bearer {token}"
    return headers
