"""
Command-Line Interface

Provides CLI commands using argparse:
- add: Add a new task
- list: Show all tasks
- complete: Mark a task done
- delete: Remove a task
"""

import argparse
import sys
from typing import Optional

from .manager import TaskManager, TaskNotFoundError
from .models import TaskStatus


# ANSI color codes for terminal output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def success(msg: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")


def error(msg: str) -> None:
    """Print an error message to stderr."""
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}", file=sys.stderr)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="task",
        description="A simple CLI task manager"
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available commands"
    )
    
    # ADD command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task description")
    
    # LIST command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--status", "-s",
        choices=["pending", "completed", "all"],
        default="all",
        help="Filter by status (default: all)"
    )
    
    # COMPLETE command
    complete_parser = subparsers.add_parser("complete", help="Mark task as done")
    complete_parser.add_argument("task_id", type=int, help="Task ID to complete")
    
    # DELETE command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID to delete")
    
    return parser


def print_tasks(tasks: list, show_header: bool = True) -> None:
    """Print tasks in a formatted table."""
    if not tasks:
        print(f"{Colors.GRAY}No tasks found.{Colors.RESET}")
        return
    
    if show_header:
        print(f"\n{Colors.BOLD}{'ID':>4}  {'Status':<10}  {'Title':<50}  {'Created':<12}{Colors.RESET}")
        print("-" * 82)
    
    for task in tasks:
        status_color = Colors.GREEN if task.status == TaskStatus.COMPLETED else Colors.YELLOW
        status_text = "Done" if task.status == TaskStatus.COMPLETED else "Pending"
        status_icon = "✓" if task.status == TaskStatus.COMPLETED else "○"
        created = task.created_at[:10]  # Just the date
        
        print(f"{task.id:>4}  {status_color}{status_icon} {status_text:<7}{Colors.RESET}  {task.title:<50}  {Colors.GRAY}{created}{Colors.RESET}")
    
    print()


def cmd_add(manager: TaskManager, title: str) -> int:
    """Handle 'add' command."""
    if not title.strip():
        error("Task title cannot be empty")
        return 1
    
    task = manager.add(title)
    success(f"Added task #{task.id}: {task.title}")
    return 0


def cmd_list(manager: TaskManager, status_filter: str) -> int:
    """Handle 'list' command."""
    status: Optional[TaskStatus] = None
    
    if status_filter == "pending":
        status = TaskStatus.PENDING
    elif status_filter == "completed":
        status = TaskStatus.COMPLETED
    
    tasks = manager.list(status)
    
    # Summary
    total = manager.count()
    pending = manager.count(TaskStatus.PENDING)
    completed = manager.count(TaskStatus.COMPLETED)
    
    print(f"\n{Colors.CYAN}Tasks: {total} total, {pending} pending, {completed} completed{Colors.RESET}")
    
    print_tasks(tasks)
    return 0


def cmd_complete(manager: TaskManager, task_id: int) -> int:
    """Handle 'complete' command."""
    try:
        task = manager.complete(task_id)
        success(f"Completed task #{task.id}: {task.title}")
        return 0
    except TaskNotFoundError as e:
        error(str(e))
        return 1


def cmd_delete(manager: TaskManager, task_id: int) -> int:
    """Handle 'delete' command."""
    try:
        task = manager.delete(task_id)
        success(f"Deleted task #{task.id}: {task.title}")
        return 0
    except TaskNotFoundError as e:
        error(str(e))
        return 1


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    manager = TaskManager()
    
    if args.command == "add":
        return cmd_add(manager, args.title)
    elif args.command == "list":
        return cmd_list(manager, args.status)
    elif args.command == "complete":
        return cmd_complete(manager, args.task_id)
    elif args.command == "delete":
        return cmd_delete(manager, args.task_id)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
