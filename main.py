from fastapi import FastAPI, HTTPException
from models import TodoCreate, Todo
from uuid import uuid4
from datetime import datetime
from models import TodoUpdate
from fastapi import status

app = FastAPI()
DB = {}

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    todo_id = str(uuid4())
    new_todo = Todo(id=todo_id, timestamp=datetime.utcnow(), completed=False, **todo.dict())
    DB[todo_id] = new_todo
    return new_todo

@app.get("/todos", response_model=list[Todo])
def get_all_todos():
    return sorted(DB.values(), key=lambda todo: todo.timestamp)

@app.get("/todos/{id}", response_model=Todo)
def get_todo_by_id(id: str):
    todo = DB.get(id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.patch("/todos/{id}", response_model=Todo)
def update_todo(id: str, updates: TodoUpdate):
    todo = DB.get(id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = updates.dict(exclude_unset=True)

    # Replace each updated field
    updated_todo = todo.copy(update=update_data)
    DB[id] = updated_todo
    return updated_todo

@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: str):
    deleted = DB.pop(id, None)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
