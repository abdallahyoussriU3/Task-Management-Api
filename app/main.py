from fastapi import FastAPI, HTTPException, Depends, Query, status
from sqlmodel import select, Session
from typing import List, Optional
from .models import Task, TaskStatus, TaskPriority
from .schemas import TaskCreate, TaskUpdate, TaskResponse
from .database import engine, get_session
from datetime import datetime
from app.routers import tasks

app = FastAPI(title="Task Management API", description="A FastAPI-based task management API.")

@app.on_event("startup")
def on_startup():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Task Management API",
        "endpoints": [
            "/health", "/tasks", "/tasks/{task_id}", "/tasks/status/{status}", "/tasks/priority/{priority}"
        ]
    }

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

app.include_router(tasks.router)
