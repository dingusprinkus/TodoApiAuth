from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import get_curr_user
from database import get_db
from models import Task, User
from schemas import TaskCreate, TaskResponse

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_curr_user),
):
    new_task = Task(title=task.title, user_id=current_user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/tasks", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db), current_user: User = Depends(get_curr_user)
):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks
