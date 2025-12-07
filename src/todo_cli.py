#!/usr/bin/env python3
"""Todo CLI - Phase 1 Console Todo App

Main entry point with argparse command-line interface
"""

import sys
import argparse
from typing import Optional
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from services.task_service import (
    add_task,
    list_tasks,
    complete_task,
    update_task,
    delete_task
)
from utils.formatters import format_task_list, format_task_single


def cmd_add(args) -> int:
    """Handle 'add' command

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for user error)
    """
    try:
        task = add_task(
            title=args.title,
            description=args.description,
            priority=args.priority,
            due_date=args.due_date
        )

        print("Task added successfully!")
        print(f"ID: {task['id']}")
        print(f"Title: {task['title']}")
        print(f"Status: {task['status']}")

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_list(args) -> int:
    """Handle 'list' command

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success)
    """
    tasks = list_tasks(
        status=args.status if hasattr(args, 'status') else None,
        priority=args.priority if hasattr(args, 'priority') else None
    )

    # Sort if specified
    if hasattr(args, 'sort_by') and args.sort_by:
        sort_key = args.sort_by
        if sort_key in ['id', 'priority', 'status']:
            tasks.sort(key=lambda t: t[sort_key])
        elif sort_key in ['title', 'due_date', 'created_at']:
            tasks.sort(key=lambda t: t[sort_key] or '')

    output = format_task_list(tasks)
    print(output)

    return 0


def cmd_complete(args) -> int:
    """Handle 'complete' command

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for user error)
    """
    try:
        task = complete_task(args.task_id)
        print(f"Task #{task['id']} marked as completed!")
        print(f"Title: {task['title']}")
        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_update(args) -> int:
    """Handle 'update' command

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for user error)
    """
    try:
        # Determine which fields were provided
        task = update_task(
            task_id=args.task_id,
            title=args.title if hasattr(args, 'title') and args.title else None,
            description=args.description if hasattr(args, 'description') else None,
            priority=args.priority if hasattr(args, 'priority') and args.priority else None,
            status=args.status if hasattr(args, 'status') and args.status else None,
            due_date=args.due_date if hasattr(args, 'due_date') else None
        )

        print(f"Task #{task['id']} updated successfully!")

        # Show which fields were updated
        updated_fields = []
        if hasattr(args, 'title') and args.title:
            updated_fields.append('title')
        if hasattr(args, 'description') and args.description is not None:
            updated_fields.append('description')
        if hasattr(args, 'priority') and args.priority:
            updated_fields.append('priority')
        if hasattr(args, 'status') and args.status:
            updated_fields.append('status')
        if hasattr(args, 'due_date') and args.due_date is not None:
            updated_fields.append('due_date')

        if updated_fields:
            print(f"Updated fields: {', '.join(updated_fields)}")

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_delete(args) -> int:
    """Handle 'delete' command

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for user error)
    """
    try:
        # Get task first to show confirmation prompt
        from services.task_service import get_task_by_id

        task = get_task_by_id(args.task_id)
        if not task:
            print(f"Error: Task with ID {args.task_id} not found", file=sys.stderr)
            return 1

        # Confirmation prompt (unless --confirm flag provided)
        if not args.confirm:
            response = input(f'Are you sure you want to delete task #{args.task_id}: "{task["title"]}"? (y/N): ')
            if response.lower() != 'y':
                print("Deletion cancelled.")
                return 0

        # Delete task
        deleted_task = delete_task(args.task_id)
        print(f"Task #{deleted_task['id']} deleted successfully!")

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog='todo',
        description='Todo CLI - Manage your tasks from the command line'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('title', type=str, help='Task title')
    parser_add.add_argument(
        '--description', '-d',
        type=str,
        help='Task description'
    )
    parser_add.add_argument(
        '--due-date',
        type=str,
        dest='due_date',
        help='Due date (format: YYYY-MM-DD)'
    )
    parser_add.add_argument(
        '--priority', '-p',
        type=str,
        choices=['low', 'medium', 'high'],
        default='medium',
        help='Task priority (default: medium)'
    )
    parser_add.set_defaults(func=cmd_add)

    # List command
    parser_list = subparsers.add_parser('list', help='List all tasks')
    parser_list.add_argument(
        '--status', '-s',
        type=str,
        choices=['pending', 'completed', 'all'],
        default='all',
        help='Filter by status (default: all)'
    )
    parser_list.add_argument(
        '--priority', '-p',
        type=str,
        choices=['low', 'medium', 'high'],
        help='Filter by priority'
    )
    parser_list.add_argument(
        '--sort-by',
        type=str,
        choices=['id', 'title', 'due_date', 'priority', 'created_at'],
        default='id',
        help='Sort tasks by field (default: id)'
    )
    parser_list.set_defaults(func=cmd_list)

    # Complete command
    parser_complete = subparsers.add_parser('complete', help='Mark a task as completed')
    parser_complete.add_argument('task_id', type=int, help='Task ID')
    parser_complete.set_defaults(func=cmd_complete)

    # Update command
    parser_update = subparsers.add_parser('update', help='Update task details')
    parser_update.add_argument('task_id', type=int, help='Task ID')
    parser_update.add_argument('--title', type=str, help='New task title')
    parser_update.add_argument('--description', type=str, help='New task description')
    parser_update.add_argument(
        '--priority',
        type=str,
        choices=['low', 'medium', 'high'],
        help='New priority'
    )
    parser_update.add_argument(
        '--status',
        type=str,
        choices=['pending', 'completed'],
        help='New status'
    )
    parser_update.add_argument(
        '--due-date',
        type=str,
        dest='due_date',
        help='New due date (format: YYYY-MM-DD)'
    )
    parser_update.set_defaults(func=cmd_update)

    # Delete command
    parser_delete = subparsers.add_parser('delete', help='Delete a task')
    parser_delete.add_argument('task_id', type=int, help='Task ID')
    parser_delete.add_argument(
        '--confirm', '-y',
        action='store_true',
        help='Skip confirmation prompt'
    )
    parser_delete.set_defaults(func=cmd_delete)

    return parser


def main() -> int:
    """Main entry point

    Returns:
        Exit code (0 for success, 1 for user error, 2 for system error)
    """
    parser = create_parser()
    args = parser.parse_args()

    # Show help if no command provided
    if not args.command:
        parser.print_help()
        return 0

    # Execute command handler
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
