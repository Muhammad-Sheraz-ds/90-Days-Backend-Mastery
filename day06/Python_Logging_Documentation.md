# Python Logging Module - Study Notes

> **Source**: [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
> **Day 6 - Backend Mastery: Exception Handling & Logging**

---

## Why Logging Over Print?

| `print()` | `logging` |
|-----------|-----------|
| Goes to stdout only | Multiple destinations (file, console, network) |
| No severity levels | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| Hard to disable | Configurable at runtime |
| No timestamps | Built-in formatting with time, module, line |
| Not thread-safe | Thread-safe by default |

---

## Logging Levels

| Level | Value | Use Case |
|-------|-------|----------|
| `DEBUG` | 10 | Detailed diagnostic info for developers |
| `INFO` | 20 | Confirmation things work as expected |
| `WARNING` | 30 | Something unexpected, but still working |
| `ERROR` | 40 | Serious problem, function failed |
| `CRITICAL` | 50 | Program may not continue |

**Messages below the configured level are ignored.**

---

## Basic Usage

```python
import logging

# Configure root logger (do once at startup)
logging.basicConfig(level=logging.INFO)

# Log messages
logging.debug("Debug message")     # Hidden (level too low)
logging.info("Server started")     # Shown
logging.warning("Disk space low")  # Shown
logging.error("Connection failed") # Shown
logging.critical("System crash")   # Shown
```

---

## Module-Level Logger (Recommended)

```python
import logging

# Create logger for this module
logger = logging.getLogger(__name__)

def process_order(order_id: int) -> None:
    logger.info(f"Processing order {order_id}")
    # ...
    logger.debug(f"Order details: {details}")
```

**Why `__name__`?** Creates hierarchical loggers matching module structure.

---

## Core Components

| Component | Purpose |
|-----------|---------|
| **Logger** | Entry point for logging calls |
| **Handler** | Where to send log records (file, console, etc.) |
| **Formatter** | How to format the message |
| **Filter** | Which records to process |

---

## basicConfig() Options

```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='app.log',
    filemode='a'  # 'w' to overwrite
)
```

### Format String Attributes

| Attribute | Meaning |
|-----------|---------|
| `%(asctime)s` | Timestamp |
| `%(name)s` | Logger name |
| `%(levelname)s` | Level (INFO, ERROR, etc.) |
| `%(message)s` | Log message |
| `%(filename)s` | Source file name |
| `%(lineno)d` | Line number |
| `%(funcName)s` | Function name |

---

## Logging to Both Console and File

```python
import logging

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler (INFO and above)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

# File handler (DEBUG and above)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(file_format)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
```

---

## Logging Exceptions

```python
try:
    risky_operation()
except Exception as e:
    # exc_info=True includes stack trace
    logger.error("Operation failed", exc_info=True)
    
    # Or use exception() which auto-includes traceback
    logger.exception("Operation failed")
```

---

## Handler Types

| Handler | Destination |
|---------|-------------|
| `StreamHandler` | Console (stdout/stderr) |
| `FileHandler` | Single file |
| `RotatingFileHandler` | File with size rotation |
| `TimedRotatingFileHandler` | File with time rotation |
| `SMTPHandler` | Email |
| `HTTPHandler` | HTTP endpoint |

### Rotating File Handler

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'app.log',
    maxBytes=5*1024*1024,  # 5 MB
    backupCount=3          # Keep 3 old files
)
```

---

## Logger Hierarchy

```
root
├── myapp
│   ├── myapp.models
│   └── myapp.views
└── urllib3
```

- Messages **propagate up** to parent loggers
- Configure handlers on root logger to catch all
- Set `logger.propagate = False` to stop propagation

---

## Backend Logging Pattern

```python
import logging

def setup_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console
            logging.FileHandler('app.log')  # File
        ]
    )

# In main entry point
if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Application started")
```

---

## Quick Reference

```python
import logging

# Setup
logging.basicConfig(level=logging.INFO, filename='app.log')
logger = logging.getLogger(__name__)

# Usage
logger.debug("Variable x = %s", x)      # Lazy formatting
logger.info("User %s logged in", user)
logger.warning("Retry attempt %d", n)
logger.error("Failed: %s", error)
logger.exception("Error with traceback")  # In except block
```
