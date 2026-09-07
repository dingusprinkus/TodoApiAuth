from fastapi import APIRouter, Depends, HTTPException
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


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_curr_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada")

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Voce nao tem permissao para editar essa tarefa!"
        )

    task.title = task_update.title

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_curr_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada")

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Voce nao tem permissao para editar essa tarefa!"
        )

    db.delete(task)
    db.commit()

    return {"detail": "Tarefa deletada com sucesso"}
