from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlmodel import select, Session
from typing import List, Optional
from datetime import datetime

from ..models import Task, TaskStatus, TaskPriority
from ..schemas import TaskCreate, TaskUpdate, TaskResponse
from ..database import get_session

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    """
    Create a new task.
    """
    try:
        db_task = Task(
            title=task.title.strip(),
            description=task.description,
            status=task.status or TaskStatus.pending,
            priority=task.priority or TaskPriority.medium,
            due_date=task.due_date,
            assigned_to=task.assigned_to,
            created_at=datetime.utcnow()
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, le=100, description="Maximum number of tasks to return"),
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by task priority"),
    session: Session = Depends(get_session)
):
    """
    List all tasks, optionally filtered by status or priority.
    Supports pagination using skip and limit.
    """
    try:
        query = select(Task)
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        
        tasks = session.exec(query.offset(skip).limit(limit)).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {str(e)}")


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, session: Session = Depends(get_session)):
    """
    Retrieve a task by its ID.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    """
    Update an existing task by its ID.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")

    update_data = task_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update.")

    try:
        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    """
    Delete a task by its ID.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    
    try:
        session.delete(task)
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")


@router.get("/status/{status}", response_model=List[TaskResponse])
async def get_tasks_by_status(status: TaskStatus, session: Session = Depends(get_session)):
    """
    Retrieve all tasks with the given status.
    """
    try:
        tasks = session.exec(select(Task).where(Task.status == status)).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks by status: {str(e)}")


@router.get("/priority/{priority}", response_model=List[TaskResponse])
async def get_tasks_by_priority(priority: TaskPriority, session: Session = Depends(get_session)):
    """
    Retrieve all tasks with the given priority.
    """
    try:
        tasks = session.exec(select(Task).where(Task.priority == priority)).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks by priority: {str(e)}")
