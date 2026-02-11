"""
Task Manager v2 — Entry Point

Usage:
    python main.py add "Buy groceries"
    python main.py add "Fix bug" --priority high
    python main.py list
    python main.py list --status pending --sort priority --reverse
    python main.py list --search "bug"
    python main.py complete 1 2 3
    python main.py delete 1
    python main.py stats
"""

import sys
from task_manager_v2.cli import main

if __name__ == "__main__":
    sys.exit(main())
