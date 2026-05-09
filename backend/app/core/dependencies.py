# --- Third-party
from fastapi import Cookie

# --- Local application
from app.core.exceptions import NotAuthenticatedError, InvalidTokenError
from app.services import auth as auth_service


async def get_current_user_id(access_token: str | None = Cookie(default=None)) -> str:
    if access_token is None:
        raise NotAuthenticatedError()
    payload = auth_service.validate_token(access_token)
    if payload is None or payload.get("type") != "access":
        raise InvalidTokenError()
    return payload["sub"]
