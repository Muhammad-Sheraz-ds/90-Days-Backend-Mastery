"""
Day 15 Exercise: First FastAPI Application
==========================================

This demonstrates:
- FastAPI setup and basic routes
- Path parameters with type annotations
- Query parameters with defaults and optional values
- HTTP methods (GET, POST)
- Custom status codes and HTTPException
- Auto-generated docs at /docs

Run with:
    uvicorn main:app --reload

Then visit:
    http://127.0.0.1:8000        → Hello World
    http://127.0.0.1:8000/docs   → Swagger UI (interactive docs)
    http://127.0.0.1:8000/redoc  → ReDoc (alternative docs)
"""

from fastapi import FastAPI, HTTPException

# ──────────────────────────────────────────────
# Step 1: Create the FastAPI instance
# ──────────────────────────────────────────────

app = FastAPI(
    title="Day 15 – First API",
    description="Learning HTTP basics with FastAPI",
    version="1.0.0",
)

# ──────────────────────────────────────────────
# In-memory data store (replaced by a DB later)
# ──────────────────────────────────────────────

items_db: dict[int, dict] = {
    1: {"id": 1, "name": "Laptop", "price": 999.99, "category": "electronics"},
    2: {"id": 2, "name": "Coffee Mug", "price": 12.50, "category": "kitchen"},
    3: {"id": 3, "name": "Notebook", "price": 5.99, "category": "office"},
    4: {"id": 4, "name": "Headphones", "price": 79.99, "category": "electronics"},
    5: {"id": 5, "name": "Water Bottle", "price": 15.00, "category": "kitchen"},
}

next_id = 6  # auto-increment counter


# ──────────────────────────────────────────────
# Route 1: Hello World (GET /)
# ──────────────────────────────────────────────

@app.get("/")
async def root():
    """Root endpoint – returns a welcome message."""
    return {
        "message": "Welcome to Day 15: First FastAPI App!",
        "docs": "Visit /docs for interactive documentation",
    }


# ──────────────────────────────────────────────
# Route 2: Health Check (GET /health)
# ──────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


# ──────────────────────────────────────────────
# Route 3: Get Item by ID (Path Parameter)
#   GET /items/{item_id}
# ──────────────────────────────────────────────

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """
    Get a single item by its ID.

    - **item_id**: integer ID of the item (path parameter)

    Returns 404 if item not found.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return items_db[item_id]


# ──────────────────────────────────────────────
# Route 4: Search Items (Query Parameters)
#   GET /search?q=laptop&category=electronics&limit=5
# ──────────────────────────────────────────────

@app.get("/search")
async def search_items(
    q: str | None = None,
    category: str | None = None,
    min_price: float = 0,
    max_price: float = 10000,
    limit: int = 10,
):
    """
    Search items with filters.

    - **q**: search query (optional, matches item name)
    - **category**: filter by category (optional)
    - **min_price**: minimum price filter (default: 0)
    - **max_price**: maximum price filter (default: 10000)
    - **limit**: max results (default: 10)
    """
    results = list(items_db.values())

    # Filter by search query
    if q:
        results = [
            item for item in results
            if q.lower() in item["name"].lower()
        ]

    # Filter by category
    if category:
        results = [
            item for item in results
            if item["category"].lower() == category.lower()
        ]

    # Filter by price range
    results = [
        item for item in results
        if min_price <= item["price"] <= max_price
    ]

    return {"query": q, "count": len(results[:limit]), "items": results[:limit]}


# ──────────────────────────────────────────────
# Route 5: List All Items (Query Params for Pagination)
#   GET /items/?skip=0&limit=10
# ──────────────────────────────────────────────

@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 10):
    """
    List all items with pagination.

    - **skip**: number of items to skip (default: 0)
    - **limit**: max items to return (default: 10)
    """
    all_items = list(items_db.values())
    return {
        "total": len(all_items),
        "skip": skip,
        "limit": limit,
        "items": all_items[skip : skip + limit],
    }


# ──────────────────────────────────────────────
# Route 6: Create an Item (POST)
#   POST /items/?name=Widget&price=9.99&category=tools
# ──────────────────────────────────────────────

@app.post("/items/", status_code=201)
async def create_item(name: str, price: float, category: str = "general"):
    """
    Create a new item (using query parameters for now).

    - **name**: item name (required)
    - **price**: item price (required)
    - **category**: item category (default: "general")

    Returns 201 Created with the new item.
    """
    global next_id
    new_item = {
        "id": next_id,
        "name": name,
        "price": price,
        "category": category,
    }
    items_db[next_id] = new_item
    next_id += 1
    return new_item


# ──────────────────────────────────────────────
# Route 7: Delete an Item (DELETE)
#   DELETE /items/{item_id}
# ──────────────────────────────────────────────

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """
    Delete an item by ID.

    Returns 204 No Content on success, 404 if not found.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    del items_db[item_id]
    return None


# ──────────────────────────────────────────────
# Route 8: Get items stats (GET /stats)
# ──────────────────────────────────────────────

@app.get("/stats")
async def get_stats():
    """Get statistics about all items."""
    all_items = list(items_db.values())
    if not all_items:
        return {"total_items": 0}

    prices = [item["price"] for item in all_items]
    categories = {}
    for item in all_items:
        cat = item["category"]
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "total_items": len(all_items),
        "avg_price": round(sum(prices) / len(prices), 2),
        "min_price": min(prices),
        "max_price": max(prices),
        "categories": categories,
    }
