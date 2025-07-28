from fastapi import FastAPI, HTTPException
from models import TodoCreate, Todo
from uuid import uuid4
from datetime import datetime

app = FastAPI()
DB = {}

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    todo_id = str(uuid4())
    new_todo = Todo(id=todo_id, timestamp=datetime.utcnow(), completed=False, **todo.dict())
    DB[todo_id] = new_todo
    return new_todo
