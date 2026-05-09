# --- Third-party
import jwt
from sqlalchemy.orm import Session

# --- Standard library
from datetime import datetime, timezone, timedelta
from uuid import UUID

# --- Local application
from app.core.config import settings
from app.core.security import hash_token, verify_token_hash, new_raw_token, verify_password
from app.core.exceptions import InvalidCredentialsError, InvalidSessionError
from app.models.models import User


def generate_token(user_id: str, token_type: str) -> str:
    now = datetime.now(timezone.utc)
    if token_type == "access":
        exp = now + timedelta(minutes=settings.JWT_EXPIRY_MINUTES)
    else:
        exp = now + timedelta(days=settings.JWT_REFRESH_EXPIRY_DAYS)
    return jwt.encode(
        {"sub": user_id, "type": token_type, "iat": now, "exp": exp},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def validate_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            leeway=settings.JWT_LEEWAY,
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def login(db: Session, identifier: str, password: str) -> tuple[str, str]:
    user = (
        db.query(User).filter(User.email == identifier).first()
        or db.query(User).filter(User.username == identifier).first()
    )
    if not user or not verify_password(password, user.hashed_pw):
        raise InvalidCredentialsError()

    access_token = generate_token(str(user.id), "access")
    refresh_token = generate_token(str(user.id), "refresh")
    user.refresh_hash = hash_token(refresh_token)
    db.commit()
    return access_token, refresh_token


def refresh(db: Session, refresh_token: str | None) -> tuple[str, str]:
    if refresh_token is None:
        raise InvalidSessionError()

    payload = validate_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise InvalidSessionError()

    user = db.get(User, UUID(payload["sub"]))
    if user is None or user.refresh_hash is None:
        raise InvalidSessionError()
    if not verify_token_hash(refresh_token, user.refresh_hash):
        raise InvalidSessionError()

    access_token = generate_token(str(user.id), "access")
    new_refresh = generate_token(str(user.id), "refresh")
    user.refresh_hash = hash_token(new_refresh)
    db.commit()
    return access_token, new_refresh


def logout(db: Session, user_id: str) -> None:
    user = db.get(User, UUID(user_id))
    if user:
        user.refresh_hash = None
        db.commit()
