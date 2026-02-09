# Additional Notes: Exception Handling & Logging

> **Day 6 - Backend Mastery: Supplementary Resources**

---

## Exception Handling Patterns for APIs

### HTTP Error Responses

```python
class HTTPError(Exception):
    """Base HTTP error with status code."""
    status_code: int = 500
    
class NotFoundError(HTTPError):
    status_code = 404
    
class BadRequestError(HTTPError):
    status_code = 400

class UnauthorizedError(HTTPError):
    status_code = 401
```

### FastAPI Exception Handler

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(HTTPError)
async def http_error_handler(request: Request, exc: HTTPError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc)}
    )
```

---

## Structured Logging for Production

### JSON Logging (better for log aggregation)

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)
```

### Usage with ELK/CloudWatch

```python
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# Output:
# {"timestamp": "2024-01-15T10:30:00", "level": "ERROR", ...}
```

---

## Correlation IDs for Request Tracing

```python
import logging
import uuid
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar('request_id', default='')

class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id.get()
        return True

# In middleware
def middleware(request):
    request_id.set(str(uuid.uuid4()))
    # ... handle request

# Format
format = '%(asctime)s [%(request_id)s] %(levelname)s %(message)s'
```

---

## Logging Best Practices

| Do | Don't |
|-----|-------|
| Use module-level loggers | Use root logger everywhere |
| Log at appropriate levels | Log everything as INFO |
| Include context (IDs, values) | Log vague messages |
| Use lazy formatting `%s` | Format strings before logging |
| Log exceptions with traceback | Swallow errors silently |
| Configure in one place | Scatter basicConfig calls |

---

## Exception Best Practices

| Do | Don't |
|-----|-------|
| Create specific exceptions | Use generic Exception |
| Include error details | Raise with no message |
| Handle at appropriate level | Catch and ignore |
| Use `finally` for cleanup | Leave resources open |
| Chain related exceptions | Lose original traceback |
| Document raised exceptions | Surprise callers |

---

## Combining Exceptions and Logging

```python
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class OperationResult:
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

def safe_operation(user_id: int) -> OperationResult:
    """Perform operation with full logging."""
    logger.info(f"Starting operation for user {user_id}")
    
    try:
        result = perform_risky_task(user_id)
        logger.info(f"Operation succeeded for user {user_id}")
        return OperationResult(success=True, data=result)
        
    except ValidationError as e:
        logger.warning(f"Validation failed for user {user_id}: {e}")
        return OperationResult(success=False, error=str(e))
        
    except DatabaseError as e:
        logger.error(f"Database error for user {user_id}", exc_info=True)
        return OperationResult(success=False, error="Internal error")
        
    except Exception as e:
        logger.critical(f"Unexpected error for user {user_id}", exc_info=True)
        raise  # Re-raise unexpected errors
```

---

## Testing Exception Handling

```python
import pytest

def test_insufficient_funds_raises():
    account = BankAccount(balance=100)
    
    with pytest.raises(InsufficientFundsError) as exc_info:
        account.withdraw(200)
    
    assert exc_info.value.balance == 100
    assert exc_info.value.amount == 200

def test_logging_on_error(caplog):
    with caplog.at_level(logging.ERROR):
        process_invalid_data()
    
    assert "validation failed" in caplog.text
```

---

## Log Configuration via Environment

```python
import os
import logging

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'app.log')

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    filename=LOG_FILE if LOG_FILE else None
)
```

---

## Key Takeaways

1. **Never use bare `except:`** — always specify exception types
2. **Use `logging` over `print()`** — configurable, levels, destinations
3. **Create custom exceptions** — clearer error handling
4. **Log at right level** — DEBUG for devs, INFO for operations, ERROR for failures
5. **Include traceback** — use `exc_info=True` or `logger.exception()`
6. **Configure once** — at application startup
7. **Use correlation IDs** — trace requests across services
