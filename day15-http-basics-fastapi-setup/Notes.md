# Additional Notes: REST API Concepts & FastAPI Patterns

> **Day 15 - Backend Mastery: HTTP Basics & FastAPI Setup**

---

## What is REST?

**REST** (Representational State Transfer) is an architectural style for designing APIs. A RESTful API:

1. **Uses HTTP methods** correctly (GET, POST, PUT, DELETE)
2. **Is stateless** — each request contains all needed info
3. **Uses resource-based URLs** — nouns, not verbs
4. **Returns appropriate status codes**

### URL Design

```
✅ Good (nouns, resource-based):
GET    /users          → List all users
GET    /users/42       → Get user 42
POST   /users          → Create user
PUT    /users/42       → Update user 42
DELETE /users/42       → Delete user 42

❌ Bad (verbs in URL):
GET    /getUsers
POST   /createUser
POST   /deleteUser/42
```

---

## Request/Response Cycle

```
1. Client sends HTTP Request
   ┌──────────────────────────────────┐
   │ GET /items/42?verbose=true       │  ← Method + Path + Query
   │ Host: api.example.com            │  ← Headers
   │ Accept: application/json         │
   └──────────────────────────────────┘

2. Server processes and returns Response
   ┌──────────────────────────────────┐
   │ HTTP/1.1 200 OK                  │  ← Status Code
   │ Content-Type: application/json   │  ← Headers
   │                                  │
   │ {"id": 42, "name": "Widget"}     │  ← Body (JSON)
   └──────────────────────────────────┘
```

---

## FastAPI vs Other Frameworks

| Feature | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| Speed | Very fast (async) | Moderate | Moderate |
| Type safety | Built-in | None | Partial |
| Auto docs | ✓ (Swagger & ReDoc) | ✗ | ✗ |
| Async | Native | Partial | Partial |
| Validation | Pydantic | Manual | Forms |
| Learning curve | Easy | Easy | Steep |

---

## Testing Your API

### 1. Browser (GET only)
Navigate to `http://127.0.0.1:8000/items/1`

### 2. Swagger UI (All methods)
Navigate to `http://127.0.0.1:8000/docs`

### 3. curl (Terminal)

```bash
# GET
curl http://127.0.0.1:8000/

# GET with query params
curl "http://127.0.0.1:8000/items/?skip=0&limit=5"

# POST with JSON body
curl -X POST http://127.0.0.1:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget", "price": 9.99}'
```

### 4. Python (httpx or requests)

```python
import httpx

# GET
response = httpx.get("http://127.0.0.1:8000/items/1")
print(response.json())

# POST
response = httpx.post(
    "http://127.0.0.1:8000/items/",
    json={"name": "Widget", "price": 9.99}
)
print(response.status_code)  # 201
```

---

## Common Patterns

### Response Status Codes in FastAPI

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

# Set specific status code
@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}

# Raise HTTP errors
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id > 100:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

### Enum for Path Parameters

```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model": model_name.value}
```

---

## Project Structure

```
day15/first_api/
├── main.py          # FastAPI app + routes
├── requirements.txt # Dependencies
└── README.md        # Usage instructions
```

For larger projects (Day 16+):

```
project/
├── main.py          # App entry point
├── models.py        # Pydantic models
├── routes/          # Route handlers
│   ├── users.py
│   └── items.py
├── services/        # Business logic
└── requirements.txt
```

---

## Key Takeaways

1. **REST** = Resources as URLs + HTTP methods for actions
2. **FastAPI** auto-validates types and generates docs
3. Test with `/docs` (Swagger UI) before writing frontend code
4. Use `HTTPException` for proper error responses
5. Separate concerns early — routes, models, services
