# --- Third-party
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# --- Standard library
from uuid import UUID

# --- Local application
from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.lists import ListCreateRequest, ListResponse
from app.services import lists as list_service

router = APIRouter(prefix="/lists", tags=["lists"])


@router.get("/", response_model=list[ListResponse])
def get_lists(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    return list_service.get_lists(db, UUID(user_id))


@router.post("/", response_model=ListResponse, status_code=201)
def create_list(
    data: ListCreateRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    return list_service.create_list(db, data.name, UUID(user_id))


@router.patch("/{list_id}", response_model=ListResponse)
def rename_list(
    list_id: UUID,
    data: ListCreateRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    return list_service.rename_list(db, list_id, data.name, UUID(user_id))


@router.delete("/{list_id}", status_code=204)
def delete_list(
    list_id: UUID,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    list_service.delete_list(db, list_id, UUID(user_id))
