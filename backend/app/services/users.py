# --- Third-party
from sqlalchemy.orm import Session

# --- Local application
from app.models.models import User
from app.core.security import hash_password
from app.core.db_utils import DatabaseUtils
from app.core.exceptions import EmailAlreadyRegisteredError, UsernameAlreadyTakenError
from app.schemas.user import UserCreate


def create_user(db: Session, data: UserCreate) -> User:
    if db.query(User).filter(User.email == data.email).first():
        raise EmailAlreadyRegisteredError()
    if db.query(User).filter(User.username == data.username).first():
        raise UsernameAlreadyTakenError()

    db_utils = DatabaseUtils(db)
    user = User(
        first_name=data.first_name.strip(),
        last_name=data.last_name.strip(),
        username=data.username.strip(),
        email=data.email.strip().lower(),
        hashed_pw=hash_password(data.password),
        is_verified=True,
    )
    return db_utils.db_create(user)
