# --- Third-party
from fastapi import FastAPI
from contextlib import asynccontextmanager

# --- Local application
from app.database import engine, verify_db_status

@asynccontextmanager
async def lifespan(app: FastAPI):
    # verify db connection on startup
    db = verify_db_status()
    if db["db"] == "unreachable":
        # prevent the app from starting
        raise RuntimeError(f"Database is unreachable: {db['error']}")
    
    print("Database connection successful")
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Lista API",
    version="1.0.0",
)

@app.get("/health")
async def health():
    db = verify_db_status()
    return {"title": "Lista", "status": "OK", **db}

