# --- Third-party
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# --- Standard library
from contextlib import asynccontextmanager

# --- Local application
from app.core.config import settings
from app.core.database import verify_db_status
from app.core.exceptions import (
    AppError,
    NotAuthenticatedError,
    InvalidTokenError,
    InvalidCredentialsError,
    InvalidSessionError,
    EmailAlreadyRegisteredError,
    UsernameAlreadyTakenError,
    ListNotFoundError,
    TaskNotFoundError,
)
from app.routers.auth import router as auth_router
from app.routers.lists import router as lists_router
from app.routers.tasks import router as tasks_router

_ERROR_MAP: dict[type[AppError], tuple[int, str]] = {
    NotAuthenticatedError: (401, "Not authenticated"),
    InvalidTokenError: (401, "Invalid or expired token"),
    InvalidCredentialsError: (401, "Invalid credentials"),
    InvalidSessionError: (401, "Invalid session"),
    EmailAlreadyRegisteredError: (409, "Email already registered"),
    UsernameAlreadyTakenError: (409, "Username already taken"),
    ListNotFoundError: (404, "List not found"),
    TaskNotFoundError: (404, "Task not found"),
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = verify_db_status()
    if db["db"] == "unreachable":
        raise RuntimeError(f"Database is unreachable: {db['error']}")
    print("Database connection successful")
    yield


app = FastAPI(lifespan=lifespan, title="Lista API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    status, detail = _ERROR_MAP.get(type(exc), (500, "Unexpected error"))
    return JSONResponse(status_code=status, content={"detail": detail})


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(auth_router, prefix="/api/v1")
app.include_router(lists_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")


@app.get("/health")
async def health():
    db = verify_db_status()
    return {"title": "Lista", "status": "OK", **db}
