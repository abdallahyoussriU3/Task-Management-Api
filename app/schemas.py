from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, timezone
from .models import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None

    @validator("title")
    def validate_title(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Title cannot be empty or whitespace only.")
        return v

    @validator("due_date")
    def validate_due_date(cls, v):
        if v and v <= datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future.")
        return v

class TaskCreate(TaskBase):
    title: str  

class TaskUpdate(TaskBase):
    pass  

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: Optional[datetime]
    due_date: Optional[datetime]
    assigned_to: Optional[str]

    class Config:
        from_attributes = True