# --- Third-party
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# --- Standard library
from uuid import UUID

# --- Local application
from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.tasks import TaskCreateRequest, TaskUpdateRequest, TaskResponse
from app.services import tasks as task_service
from app.services import lists as list_service

router = APIRouter(prefix="/lists/{list_id}/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    list_id: UUID,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    list_service.get_list(db, list_id, UUID(user_id))
    return task_service.get_tasks(db, list_id)


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    list_id: UUID,
    data: TaskCreateRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    list_service.get_list(db, list_id, UUID(user_id))
    return task_service.create_task(db, list_id, data.description)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    list_id: UUID,
    task_id: UUID,
    data: TaskUpdateRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    list_service.get_list(db, list_id, UUID(user_id))
    return task_service.update_task(
        db, task_id, list_id,
        description=data.description,
        position=data.position,
        is_complete=data.is_complete,
    )


@router.delete("/{task_id}", status_code=204)
def delete_task(
    list_id: UUID,
    task_id: UUID,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    list_service.get_list(db, list_id, UUID(user_id))
    task_service.delete_task(db, task_id, list_id)
