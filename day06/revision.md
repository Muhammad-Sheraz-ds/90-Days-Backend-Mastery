# Day 6 Revision: Exception Handling & Logging
> ⏱️ 2-Minute Quick Recap

---

## EXCEPTION HANDLING

**Definition**: Mechanism to handle runtime errors gracefully without crashing.

**Why?**
- Production apps must never crash silently
- Provide meaningful error messages
- Release resources properly (files, connections)
- Enable debugging with tracebacks

### Try/Except/Else/Finally

```python
try:
    result = risky_operation()
except ValueError as e:
    handle_error(e)
else:
    # Only runs if NO exception
    process(result)
finally:
    # ALWAYS runs
    cleanup()
```

| Block | When it runs |
|-------|--------------|
| `try` | Always (may stop early) |
| `except` | Only if matching exception |
| `else` | Only if NO exception |
| `finally` | ALWAYS (cleanup) |

### Raising Exceptions

```python
raise ValueError("Invalid input")    # Raise new
raise                                 # Re-raise current
raise NewError() from original_error  # Chain exceptions
```

### Custom Exceptions

```python
class InsufficientFundsError(Exception):
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Balance ${balance}, need ${amount}")
```

**Rules**: Inherit from `Exception`, name ends with `Error`.

---

## LOGGING

**Definition**: Recording events during program execution for monitoring/debugging.

**Why over print()?**
- Severity levels (DEBUG, INFO, ERROR)
- Multiple outputs (console, file)
- Timestamps and context
- Can be disabled/configured at runtime

### Logging Levels

| Level | Value | When to use |
|-------|-------|-------------|
| DEBUG | 10 | Detailed diagnostic info |
| INFO | 20 | Things working as expected |
| WARNING | 30 | Something unexpected |
| ERROR | 40 | Function failed |
| CRITICAL | 50 | Program may crash |

### Basic Setup

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)
```

### Usage

```python
logger.info("User logged in")
logger.warning("Retry attempt 3")
logger.error("Connection failed")
logger.exception("Error with traceback")  # In except block
```

### Console + File

```python
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())       # Console
logger.addHandler(logging.FileHandler('app.log'))  # File
```

---

## COMBINING BOTH

```python
try:
    process_order(order_id)
    logger.info(f"Order {order_id} processed")
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
except Exception as e:
    logger.error("Unexpected error", exc_info=True)
    raise
```

---

## COMMON MISTAKES

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `except:` (bare) | `except Exception as e:` |
| `except: pass` | Handle or re-raise |
| `print("error")` | `logger.error()` |
| Catch everything | Catch specific exceptions |

---

## KEY TERMS

| Term | One-liner |
|------|-----------|
| Exception | Runtime error that can be caught |
| try/except | Handle exceptions gracefully |
| finally | Cleanup code that always runs |
| raise | Trigger an exception |
| Custom exception | User-defined error class |
| Logger | Object that records events |
| Handler | Where logs go (console/file) |
| Formatter | How logs appear |
| Level | Severity (DEBUG→CRITICAL) |
