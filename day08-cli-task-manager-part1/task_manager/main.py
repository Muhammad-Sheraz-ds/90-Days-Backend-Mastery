"""
Task Manager - Main Entry Point

Run with:
    python main.py add "Buy groceries"
    python main.py list
    python main.py complete 1
    python main.py delete 1
"""

import sys
from task_manager.cli import main

if __name__ == "__main__":
    sys.exit(main())
