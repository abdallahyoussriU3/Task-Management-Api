from pydantic import BaseModel, Field, validator, Extra
from typing import Optional
from datetime import datetime, timezone
from .models import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    """
    Shared base model for tasks, used for creation and update.
    """
    title: Optional[str] = Field(
        default=None,
        description="Short title of the task",
        example="Implement user login"
    )
    description: Optional[str] = Field(
        default=None,
        description="Detailed description of what the task involves",
        example="Develop login functionality using FastAPI and JWT."
    )
    status: Optional[TaskStatus] = Field(
        default=None,
        description="Current task status. Must be one of: 'pending', 'in_progress', 'completed', 'cancelled'",
        example="pending"
    )
    priority: Optional[TaskPriority] = Field(
        default=None,
        description="Task priority level. Must be one of: 'low', 'medium', 'high', 'urgent'",
        example="high"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Due date for the task in UTC. Must be a future datetime.",
        example="2025-08-15T17:00:00Z"
    )
    assigned_to: Optional[str] = Field(
        default=None,
        description="User ID or username of the person assigned to this task",
        example="user_123"
    )

    @validator("title")
    def validate_title(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Title cannot be empty or whitespace only.")
        return v

    @validator("due_date")
    def validate_due_date(cls, v):
        if v:
            # If v is naive, make it aware (assume UTC)
            if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
                v = v.replace(tzinfo=timezone.utc)
            if v <= datetime.now(timezone.utc):
                raise ValueError("Due date must be in the future.")
        return v

    class Config:
        extra = Extra.forbid  # Disallow extra/undefined fields


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    title: str = Field(
        ...,
        description="Title of the task (required)",
        example="Fix PayPal integration bug"
    )

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "title": "Fix PayPal integration bug",
                "description": "Resolve issues with transaction failures during PayPal checkout",
                "status": "pending",
                "priority": "urgent",
                "due_date": "2025-08-01T23:59:59Z",
                "assigned_to": "backend_dev_01"
            }
        }


class TaskUpdate(TaskBase):
    """
    Schema for updating an existing task. All fields are optional.
    """
    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "description": "Updated task details after review",
                "status": "in_progress",
                "priority": "medium",
                "due_date": "2025-08-10T12:00:00Z"
            }
        }


class TaskResponse(BaseModel):
    """
    Schema for returning task details in API responses.
    Fields are ordered to show ID first, followed by metadata and content.
    """
    id: int = Field(..., description="Unique identifier of the task", example=42)
    
    
    title: Optional[str] = Field(None, description="Short title of the task", example="Implement user login")
    description: Optional[str] = Field(None, description="Detailed task description", example="Use JWT for secure login")
    status: Optional[TaskStatus] = Field(None, description="Current status of the task", example="pending")
    priority: Optional[TaskPriority] = Field(None, description="Priority level of the task", example="high")
    due_date: Optional[datetime] = Field(None, description="Deadline (UTC)", example="2025-08-15T17:00:00Z")
    assigned_to: Optional[str] = Field(None, description="User ID of the assignee", example="user_123")
    
    created_at: datetime = Field(..., description="Timestamp when the task was created", example="2025-07-01T10:00:00Z")
    updated_at: Optional[datetime] = Field(None, description="Timestamp of the last update", example="2025-07-02T15:30:00Z")

    class Config:
        from_attributes = True
        extra = Extra.forbid
