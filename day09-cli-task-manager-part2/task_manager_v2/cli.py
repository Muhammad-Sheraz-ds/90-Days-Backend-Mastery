"""
CLI Interface (v2) — Enhanced with filtering, sorting, search, and polished output.

Commands:
    add     — Add a new task (with optional priority)
    list    — List tasks (filter by status/priority, sort, search)
    complete — Mark task(s) as done
    delete  — Remove a task
    stats   — Show task statistics
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

from .manager import TaskManager, TaskNotFoundError, ValidationError
from .models import TaskStatus, Priority


# ============================================================================
# Terminal Colors
# ============================================================================

class C:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    MAGENTA = "\033[95m"


def success(msg: str) -> None:
    print(f"{C.GREEN}✓{C.RESET} {msg}")

def error(msg: str) -> None:
    print(f"{C.RED}✗ Error:{C.RESET} {msg}", file=sys.stderr)

def info(msg: str) -> None:
    print(f"{C.CYAN}ℹ{C.RESET} {msg}")


# ============================================================================
# Table Printer
# ============================================================================

def print_tasks(tasks: list) -> None:
    """Print tasks in a formatted table with colors."""
    if not tasks:
        print(f"\n{C.GRAY}  No tasks found.{C.RESET}\n")
        return
    
    # Header
    print(f"\n{C.BOLD}{'ID':>4}  {'Pri':<4}  {'Status':<12}  {'Title':<45}  {'Created':<12}{C.RESET}")
    print("─" * 85)
    
    for t in tasks:
        # Priority color
        pri_colors = {"high": C.RED, "medium": C.YELLOW, "low": C.GRAY}
        pri_display = {"high": "!!!", "medium": "!! ", "low": "!  "}
        pri_c = pri_colors[t.priority.value]
        pri_d = pri_display[t.priority.value]
        
        # Status
        if t.status == TaskStatus.COMPLETED:
            status_str = f"{C.GREEN}✓ Done   {C.RESET}"
        else:
            status_str = f"{C.YELLOW}○ Pending{C.RESET}"
        
        date = t.created_at[:10]
        
        print(f"{t.id:>4}  {pri_c}{pri_d}{C.RESET}  {status_str}   {t.title:<45}  {C.GRAY}{date}{C.RESET}")
    
    print()


# ============================================================================
# Parser Setup
# ============================================================================

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task",
        description="CLI Task Manager (v2) — with filtering, sorting & search",
        epilog="""
Examples:
  python main.py add "Buy groceries"
  python main.py add "Fix critical bug" --priority high
  python main.py list --status pending --sort priority --reverse
  python main.py list --search "bug"
  python main.py complete 1 2 3
  python main.py stats
"""
    )
    
    subs = parser.add_subparsers(dest="command", title="commands")
    
    # ---- ADD ----
    p_add = subs.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task description")
    p_add.add_argument(
        "--priority", "-p",
        choices=["low", "medium", "high"],
        default="medium",
        help="Task priority (default: medium)"
    )
    
    # ---- LIST ----
    p_list = subs.add_parser("list", aliases=["ls"], help="List tasks")
    p_list.add_argument(
        "--status", "-s",
        choices=["pending", "completed", "all"],
        default="all",
        help="Filter by status"
    )
    p_list.add_argument(
        "--priority", "-p",
        choices=["low", "medium", "high"],
        help="Filter by priority"
    )
    p_list.add_argument(
        "--sort",
        choices=["id", "date", "title", "status", "priority"],
        default="id",
        help="Sort by field (default: id)"
    )
    p_list.add_argument(
        "--reverse", "-r",
        action="store_true",
        help="Reverse sort order"
    )
    p_list.add_argument(
        "--search", "-q",
        help="Search tasks by title"
    )
    
    # ---- COMPLETE ----
    p_done = subs.add_parser("complete", aliases=["done"], help="Mark task(s) as done")
    p_done.add_argument("task_ids", type=int, nargs="+", help="Task ID(s) to complete")
    
    # ---- DELETE ----
    p_del = subs.add_parser("delete", aliases=["rm"], help="Delete a task")
    p_del.add_argument("task_id", type=int, help="Task ID to delete")
    
    # ---- STATS ----
    subs.add_parser("stats", help="Show task statistics")
    
    return parser


# ============================================================================
# Command Handlers
# ============================================================================

def cmd_add(manager: TaskManager, args) -> int:
    try:
        task = manager.add(args.title, args.priority)
        success(f"Added task #{task.id}: {task.title} [{args.priority}]")
        return 0
    except ValidationError as e:
        error(str(e))
        return 1


def cmd_list(manager: TaskManager, args) -> int:
    # Search overrides filters
    if args.search:
        tasks = manager.search(args.search)
        info(f"Search results for '{args.search}':")
    else:
        # Apply filters
        status = None
        if args.status != "all":
            status = TaskStatus(args.status)
        
        priority = None
        if args.priority:
            priority = Priority(args.priority)
        
        tasks = manager.list(status=status, priority=priority)
    
    # Sort
    tasks = manager.sorted_list(tasks, sort_by=args.sort, reverse=args.reverse)
    
    # Summary
    stats = manager.stats()
    print(f"\n{C.CYAN}Tasks: {stats['total']} total, {stats['pending']} pending, {stats['completed']} completed{C.RESET}")
    
    print_tasks(tasks)
    return 0


def cmd_complete(manager: TaskManager, args) -> int:
    exit_code = 0
    for tid in args.task_ids:
        try:
            task = manager.complete(tid)
            success(f"Completed #{tid}: {task.title}")
        except TaskNotFoundError:
            error(f"Task #{tid} not found. Use 'list' to see available tasks.")
            exit_code = 1
    return exit_code


def cmd_delete(manager: TaskManager, args) -> int:
    try:
        task = manager.delete(args.task_id)
        success(f"Deleted #{args.task_id}: {task.title}")
        return 0
    except TaskNotFoundError:
        error(f"Task #{args.task_id} not found. Use 'list' to see available tasks.")
        return 1


def cmd_stats(manager: TaskManager) -> int:
    stats = manager.stats()
    print(f"\n{C.BOLD}📊 Task Statistics{C.RESET}")
    print(f"{'─' * 30}")
    print(f"  Total:         {stats['total']}")
    print(f"  {C.YELLOW}Pending:       {stats['pending']}{C.RESET}")
    print(f"  {C.GREEN}Completed:     {stats['completed']}{C.RESET}")
    print(f"  {C.RED}High Priority: {stats['high_priority']}{C.RESET}")
    
    if stats['total'] > 0:
        pct = (stats['completed'] / stats['total']) * 100
        print(f"  Progress:      {pct:.0f}%")
    print()
    return 0


# ============================================================================
# Main Entry
# ============================================================================

def main() -> int:
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        manager = TaskManager()
    except Exception as e:
        error(f"Failed to initialize: {e}")
        return 1
    
    commands = {
        "add": lambda: cmd_add(manager, args),
        "list": lambda: cmd_list(manager, args),
        "ls": lambda: cmd_list(manager, args),
        "complete": lambda: cmd_complete(manager, args),
        "done": lambda: cmd_complete(manager, args),
        "delete": lambda: cmd_delete(manager, args),
        "rm": lambda: cmd_delete(manager, args),
        "stats": lambda: cmd_stats(manager),
    }
    
    handler = commands.get(args.command)
    if handler:
        return handler()
    
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
