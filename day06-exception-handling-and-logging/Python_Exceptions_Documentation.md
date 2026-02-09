# Python Exceptions Documentation - Study Notes

> **Source**: [Python Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
> **Day 6 - Backend Mastery: Exception Handling & Logging**

---

## Two Types of Errors

| Type | When | Example |
|------|------|---------|
| **Syntax Error** | Before execution (parsing) | `while True print('Hi')` — missing `:` |
| **Exception** | During execution (runtime) | `10 / 0` → ZeroDivisionError |

---

## Common Built-in Exceptions

| Exception | Cause |
|-----------|-------|
| `ZeroDivisionError` | Division by zero |
| `NameError` | Variable not defined |
| `TypeError` | Wrong type operation |
| `ValueError` | Right type, wrong value |
| `KeyError` | Dict key not found |
| `IndexError` | List index out of range |
| `FileNotFoundError` | File doesn't exist |
| `OSError` | OS-level error |

---

## Try/Except/Else/Finally

```python
try:
    # Code that might raise an exception
    result = risky_operation()
except ValueError:
    # Handle specific exception
    print("Invalid value")
except (TypeError, KeyError) as e:
    # Handle multiple exceptions
    print(f"Error: {e}")
except Exception as e:
    # Catch-all (use sparingly)
    print(f"Unexpected error: {e}")
    raise  # Re-raise after logging
else:
    # Runs ONLY if no exception occurred
    print("Success!")
finally:
    # ALWAYS runs (cleanup)
    close_connection()
```

### Execution Flow

| Scenario | try | except | else | finally |
|----------|-----|--------|------|---------|
| No exception | ✅ | ❌ | ✅ | ✅ |
| Handled exception | Partial | ✅ | ❌ | ✅ |
| Unhandled exception | Partial | ❌ | ❌ | ✅ + re-raise |

---

## Raising Exceptions

```python
# Raise with message
raise ValueError("Amount must be positive")

# Raise without message
raise ValueError

# Re-raise current exception
except SomeError:
    log_error()
    raise
```

---

## Exception Chaining

**Implicit chaining** (during handling):
```python
try:
    open("db.sqlite")
except OSError:
    raise RuntimeError("DB error")  # Shows both tracebacks
```

**Explicit chaining** (`from`):
```python
except ConnectionError as exc:
    raise RuntimeError("Failed to connect") from exc
```

**Disable chaining**:
```python
raise RuntimeError("Clean error") from None
```

---

## User-Defined Exceptions

```python
class BankError(Exception):
    """Base exception for banking operations."""
    pass

class InsufficientFundsError(BankError):
    """Raised when withdrawal exceeds balance."""
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"Cannot withdraw ${amount:.2f}, balance is ${balance:.2f}"
        )

class NegativeAmountError(BankError):
    """Raised when amount is negative."""
    def __init__(self, amount: float):
        super().__init__(f"Amount cannot be negative: {amount}")
```

### Naming Convention
- End with `Error` suffix
- Inherit from `Exception` (not `BaseException`)
- Keep simple: store relevant data as attributes

---

## The 'with' Statement (Context Manager)

Automatic cleanup even if exceptions occur:

```python
# Without 'with' — risky
f = open("file.txt")
data = f.read()
f.close()  # May never run if error above

# With 'with' — safe
with open("file.txt") as f:
    data = f.read()
# File automatically closed
```

**Works with**: files, locks, database connections, network sockets

---

## Exception Hierarchy (Simplified)

```
BaseException
├── SystemExit
├── KeyboardInterrupt
└── Exception
    ├── ValueError
    ├── TypeError
    ├── KeyError
    ├── OSError
    │   └── FileNotFoundError
    └── YourCustomError
```

> **Rule**: Always catch `Exception`, never `BaseException` (would catch Ctrl+C).

---

## Backend Best Practices

| Practice | Reason |
|----------|--------|
| Be specific with exceptions | Don't catch everything blindly |
| Log before re-raising | Preserve context for debugging |
| Use custom exceptions | Clear error types for API responses |
| Always use `with` for resources | Prevents resource leaks |
| Never silence exceptions | `except: pass` hides bugs |

---

## Pattern: Exception + Logging

```python
import logging

logger = logging.getLogger(__name__)

def withdraw(amount: float) -> None:
    try:
        if amount <= 0:
            raise NegativeAmountError(amount)
        # ... perform withdrawal
        logger.info(f"Withdrew ${amount:.2f}")
    except NegativeAmountError as e:
        logger.error(f"Withdrawal failed: {e}")
        raise
```
