# FastAPI First Steps

> **Source**: [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
> **Day 15 - Backend Mastery: HTTP Basics & FastAPI Setup**

---

## What is FastAPI?

**FastAPI** is a modern, high-performance Python web framework for building APIs. It's built on:
- **Starlette** (ASGI framework for async support)
- **Pydantic** (data validation using type hints)

**Why FastAPI?**
- Fastest-growing Python framework (2025)
- Auto-generates interactive API docs (Swagger UI + ReDoc)
- Type-safe with Python type hints
- Built-in data validation
- Async support out of the box

---

## Installation

```bash
# Install FastAPI with all standard dependencies
pip install "fastapi[standard]"

# This includes uvicorn (ASGI server), pydantic, etc.
```

---

## Hello World — The Simplest API

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### Run It

```bash
# Development mode (auto-reload on file changes)
uvicorn main:app --reload

# Or using FastAPI CLI
fastapi dev main.py
```

Server starts at: `http://127.0.0.1:8000`

### Step-by-Step Breakdown

| Step | Code | What It Does |
|------|------|-------------|
| 1 | `from fastapi import FastAPI` | Import the framework |
| 2 | `app = FastAPI()` | Create the app instance |
| 3 | `@app.get("/")` | Decorator: handle GET requests to `/` |
| 4 | `async def root():` | Define the handler function |
| 5 | `return {"message": ...}` | Return JSON response |

---

## Path Parameters

Parameters embedded in the URL path itself.

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

- URL: `GET /items/42` → `{"item_id": 42}`
- URL: `GET /items/foo` → **422 Error** (not a valid int)

### Type Annotations = Auto Conversion + Validation

```python
# item_id declared as int → FastAPI automatically:
# 1. Converts string "42" from URL to Python int 42
# 2. Validates that it IS an integer
# 3. Returns 422 error if not
```

### Multiple Path Parameters

```python
@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: int):
    return {"user_id": user_id, "item_id": item_id}
```

---

## Query Parameters

Parameters passed after `?` in the URL. Any function parameter NOT in the path is automatically a query parameter.

```python
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

- URL: `GET /items/?skip=0&limit=2` → Returns first 2 items
- URL: `GET /items/` → Uses defaults: skip=0, limit=10

### Optional Query Parameters

```python
from typing import Optional

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

- URL: `GET /items/5` → `{"item_id": 5}`
- URL: `GET /items/5?q=search` → `{"item_id": 5, "q": "search"}`

### Boolean Query Parameters

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int, short: bool = False):
    item = {"item_id": item_id}
    if not short:
        item["description"] = "This item has a long description"
    return item
```

All of these evaluate to `True`: `?short=1`, `?short=True`, `?short=true`, `?short=yes`, `?short=on`

---

## Path Operation Decorators

Each HTTP method has a corresponding decorator:

```python
@app.get("/items/")       # Read
@app.post("/items/")      # Create
@app.put("/items/{id}")   # Update (full)
@app.patch("/items/{id}") # Update (partial)
@app.delete("/items/{id}")# Delete
```

---

## Auto-Generated Documentation

FastAPI automatically generates interactive API docs:

| URL | UI | Description |
|-----|------|-------------|
| `/docs` | Swagger UI | Interactive, try endpoints live |
| `/redoc` | ReDoc | Clean, readable documentation |
| `/openapi.json` | Raw JSON | OpenAPI 3.0 schema |

Both are generated from your code — **no extra work needed!**

---

## async vs Regular Functions

FastAPI supports **both**:

```python
# Async (for I/O-bound operations)
@app.get("/")
async def read_root():
    return {"message": "Hello"}

# Regular (works fine too)
@app.get("/")
def read_root():
    return {"message": "Hello"}
```

**Rule of thumb**: Use `async def` when doing async I/O (databases, HTTP calls). Use `def` for CPU-bound or simple operations.

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| `FastAPI()` | Creates the app instance |
| `@app.get("/path")` | Path operation decorator |
| `{param}` in path | Path parameter (required) |
| Function param not in path | Query parameter |
| Type hints (`int`, `str`) | Auto conversion + validation |
| `param: str \| None = None` | Optional query parameter |
| `uvicorn main:app --reload` | Run dev server |
| `/docs` | Swagger UI auto-docs |
