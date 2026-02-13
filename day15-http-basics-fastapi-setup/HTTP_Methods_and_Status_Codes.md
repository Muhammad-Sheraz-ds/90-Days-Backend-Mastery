# HTTP Methods & Status Codes

> **Source**: [MDN HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) + [MDN HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
> **Day 15 - Backend Mastery: HTTP Basics & FastAPI Setup**

---

## What is HTTP?

**HTTP** (HyperText Transfer Protocol) is the protocol used for communication between a client (browser, app, Postman) and a server. Every API request follows this pattern:

```
Client  ──── HTTP Request ────►  Server
        (Method + URL + Body)
        
Client  ◄── HTTP Response ────  Server
        (Status Code + Body)
```

---

## HTTP Methods (Verbs)

HTTP defines **request methods** indicating what action the client wants to perform.

### Core Methods for APIs

| Method | Purpose | Has Body? | Idempotent? | Safe? |
|--------|---------|-----------|-------------|-------|
| **GET** | Read/retrieve data | ✗ | ✓ | ✓ |
| **POST** | Create new resource | ✓ | ✗ | ✗ |
| **PUT** | Replace entire resource | ✓ | ✓ | ✗ |
| **PATCH** | Partial update | ✓ | ✗ | ✗ |
| **DELETE** | Remove resource | ✗ | ✓ | ✗ |

### What Do "Safe" and "Idempotent" Mean?

- **Safe**: Does NOT change server state. GET only reads data.
- **Idempotent**: Multiple identical requests produce the same result.
  - `DELETE /users/5` → Deleting user 5 twice still means user 5 is gone.
  - `POST /users` → Creating twice creates **two** users (not idempotent).

### CRUD Mapping

| Operation | HTTP Method | URL Example | Description |
|-----------|-------------|-------------|-------------|
| **C**reate | `POST` | `POST /users` | Create a new user |
| **R**ead all | `GET` | `GET /users` | Get all users |
| **R**ead one | `GET` | `GET /users/1` | Get user with ID 1 |
| **U**pdate | `PUT` | `PUT /users/1` | Replace user 1 |
| **U**pdate partial | `PATCH` | `PATCH /users/1` | Update some fields |
| **D**elete | `DELETE` | `DELETE /users/1` | Remove user 1 |

---

## HTTP Status Codes

Status codes are **3-digit numbers** in every HTTP response telling the client what happened.

### Categories

| Range | Category | Meaning |
|-------|----------|---------|
| **1xx** | Informational | Request received, continuing |
| **2xx** | Success | Request was successful |
| **3xx** | Redirection | Client must take additional action |
| **4xx** | Client Error | Problem with the request |
| **5xx** | Server Error | Server failed to fulfill request |

### Must-Know Status Codes

#### ✅ Success (2xx)

| Code | Name | When to Use |
|------|------|-------------|
| **200** | OK | Standard success (GET, PUT, PATCH) |
| **201** | Created | New resource created (POST) |
| **204** | No Content | Success but nothing to return (DELETE) |

#### ❌ Client Errors (4xx)

| Code | Name | When to Use |
|------|------|-------------|
| **400** | Bad Request | Invalid input / malformed request |
| **401** | Unauthorized | Not authenticated (no/invalid token) |
| **403** | Forbidden | Authenticated but no permission |
| **404** | Not Found | Resource doesn't exist |
| **405** | Method Not Allowed | Wrong HTTP method for endpoint |
| **409** | Conflict | Conflicting state (e.g., duplicate) |
| **422** | Unprocessable Entity | Validation error (FastAPI default) |

#### 💥 Server Errors (5xx)

| Code | Name | When to Use |
|------|------|-------------|
| **500** | Internal Server Error | Unhandled exception on server |
| **502** | Bad Gateway | Upstream server returned invalid response |
| **503** | Service Unavailable | Server overloaded / maintenance |

---

## Anatomy of an HTTP Request

```
POST /api/users HTTP/1.1          ← Method + Path + Protocol
Host: api.example.com             ← Headers
Content-Type: application/json
Authorization: Bearer abc123

{                                 ← Body (JSON)
    "name": "Alice",
    "email": "alice@example.com"
}
```

## Anatomy of an HTTP Response

```
HTTP/1.1 201 Created              ← Status Line
Content-Type: application/json    ← Headers
Location: /api/users/42

{                                 ← Body (JSON)
    "id": 42,
    "name": "Alice",
    "email": "alice@example.com"
}
```

---

## Common Headers

| Header | Purpose | Example |
|--------|---------|---------|
| `Content-Type` | Body format | `application/json` |
| `Authorization` | Authentication | `Bearer <token>` |
| `Accept` | Desired response format | `application/json` |
| `Location` | URL of created resource | `/users/42` |

---

## Key Takeaways

1. **GET** = read, **POST** = create, **PUT** = replace, **PATCH** = partial update, **DELETE** = remove
2. **2xx** = success, **4xx** = client error, **5xx** = server error
3. Use **201** for creation, **204** for deletion, **404** for not found
4. FastAPI returns **422** for validation errors by default
5. **Idempotent** means repeating the same request gives the same result
