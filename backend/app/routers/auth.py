# --- Third-party
from fastapi import APIRouter, Depends, Response, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# --- Local application
from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate, UserCreateResponse
from app.services import auth as auth_service
from app.services import users as user_service

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie("access_token", access_token, httponly=True, samesite="lax", secure=False)
    response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="lax", secure=False)


@router.post("/register", response_model=UserCreateResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, data)


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    access_token, refresh_token = auth_service.login(db, data.identifier, data.password)
    response = JSONResponse(content={"message": "Logged in"})
    _set_auth_cookies(response, access_token, refresh_token)
    return response


@router.post("/refresh")
def refresh(refresh_token: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    access_token, new_refresh = auth_service.refresh(db, refresh_token)
    response = JSONResponse(content={"message": "Token refreshed"})
    _set_auth_cookies(response, access_token, new_refresh)
    return response


@router.post("/logout", status_code=204)
def logout(
    response: Response,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    auth_service.logout(db, user_id)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
