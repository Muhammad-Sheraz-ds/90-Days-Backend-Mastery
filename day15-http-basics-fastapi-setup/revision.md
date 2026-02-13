# Day 15 Revision: HTTP Basics & FastAPI Setup

> Quick-fire review — test yourself before moving to Day 16!

---

## Section 1: HTTP Methods (Fill in the Blank)

1. `___` is used to **read** data from a server.
2. `___` is used to **create** a new resource.
3. `___` replaces the **entire** resource.
4. `___` applies a **partial** modification.
5. `___` removes a resource from the server.

<details>
<summary>Answers</summary>

1. GET
2. POST
3. PUT
4. PATCH
5. DELETE
</details>

---

## Section 2: Status Codes (Match the Code)

Match each scenario to its status code:

| Scenario | Code |
|----------|------|
| a) Successful GET request | ___ |
| b) Resource created via POST | ___ |
| c) Deleted successfully, no body | ___ |
| d) Client sent invalid JSON | ___ |
| e) Resource not found | ___ |
| f) Server crashed unexpectedly | ___ |
| g) User not logged in | ___ |

<details>
<summary>Answers</summary>

| Scenario | Code |
|----------|------|
| a) | 200 OK |
| b) | 201 Created |
| c) | 204 No Content |
| d) | 400 Bad Request |
| e) | 404 Not Found |
| f) | 500 Internal Server Error |
| g) | 401 Unauthorized |
</details>

---

## Section 3: True or False

1. T/F: GET requests are **idempotent** and **safe**.
2. T/F: POST requests are **idempotent**.
3. T/F: DELETE requests are **idempotent**.
4. T/F: 4xx errors are the **server's** fault.
5. T/F: FastAPI auto-generates Swagger docs at `/docs`.

<details>
<summary>Answers</summary>

1. **True** — GET doesn't change state and repeating it yields same result.
2. **False** — POST creates a new resource each time.
3. **True** — Deleting the same resource twice gives the same end state.
4. **False** — 4xx errors are the **client's** fault. 5xx are server errors.
5. **True** — Swagger UI is available at `/docs` automatically.
</details>

---

## Section 4: FastAPI Code Review

### What's wrong with this code?

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id):     # <-- Issue here
    return {"user_id": user_id}
```

<details>
<summary>Answer</summary>

**Missing type annotation!** Without `user_id: int`, FastAPI treats it as a string and won't validate it.

Fix:
```python
async def get_user(user_id: int):
```
</details>

---

### What will this return for `GET /items/?limit=2`?

```python
db = [{"name": "A"}, {"name": "B"}, {"name": "C"}]

@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 10):
    return db[skip : skip + limit]
```

<details>
<summary>Answer</summary>

```json
[{"name": "A"}, {"name": "B"}]
```

`skip=0` (default), `limit=2` (from query) → returns first 2 items.
</details>

---

### How do you return a 404 error in FastAPI?

<details>
<summary>Answer</summary>

```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Item not found")
```
</details>

---

## Section 5: Quick Reference

```
# Install
pip install "fastapi[standard]"

# Run dev server
uvicorn main:app --reload

# Auto-docs
http://127.0.0.1:8000/docs       (Swagger UI)
http://127.0.0.1:8000/redoc      (ReDoc)

# HTTP Methods → Decorators
@app.get()     → Read
@app.post()    → Create
@app.put()     → Update (full)
@app.patch()   → Update (partial)
@app.delete()  → Delete
```

---

## Section 6: What You Built Today

- ✅ Learned HTTP methods and their CRUD mapping
- ✅ Understood status codes (200, 201, 204, 400, 404, 500)
- ✅ Installed FastAPI and Uvicorn
- ✅ Created routes with path params (`/items/{id}`)
- ✅ Created routes with query params (`/search?q=laptop`)
- ✅ Explored auto-generated docs at `/docs`

## Next: Day 16 — Pydantic Models

You'll learn to use **Pydantic** for request/response models with validation (replace query params with proper JSON bodies!).
