# Task Management API

A FastAPI-based task management API using SQLModel and SQLite.

## Features

- CRUD operations for tasks
- Filtering, pagination, and validation
- Automatic API docs

## Setup Instructions

```bash
pip install -r requirements.txt

# Run the application
python main.py

# Access API documentation
http://localhost:8000/docs
```

## Example API Call

```bash
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Sample Task", "priority": "high"}'
```
