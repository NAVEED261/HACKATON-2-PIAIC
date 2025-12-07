"""Output formatting utilities for CLI display

Provides table and single-task formatting functions
"""

from typing import List, Dict


def format_task_list(tasks: List[Dict], show_header: bool = True) -> str:
    """Format list of tasks as a table

    Args:
        tasks: List of task dictionaries
        show_header: Whether to show table header (default: True)

    Returns:
        Formatted string with task table
    """
    if not tasks:
        return "No tasks found."

    lines = []

    if show_header:
        # Table header
        header = f"{'ID':<6}{'Title':<32}{'Status':<13}{'Priority':<12}{'Due Date':<12}"
        separator = "-" * 75
        lines.append(header)
        lines.append(separator)

    # Table rows
    for task in tasks:
        task_id = str(task['id'])
        title = task['title'][:30]  # Truncate long titles
        status = task['status']
        priority = task['priority']
        due_date = task.get('due_date') or 'N/A'

        row = f"{task_id:<6}{title:<32}{status:<13}{priority:<12}{due_date:<12}"
        lines.append(row)

    # Summary line
    total = len(tasks)
    pending_count = sum(1 for t in tasks if t['status'] == 'pending')
    completed_count = sum(1 for t in tasks if t['status'] == 'completed')

    if total == 1:
        summary = f"\nTotal: 1 task"
    else:
        summary = f"\nTotal: {total} tasks ({pending_count} pending, {completed_count} completed)"

    lines.append(summary)

    return '\n'.join(lines)


def format_task_single(task: Dict) -> str:
    """Format a single task for display

    Args:
        task: Task dictionary

    Returns:
        Formatted string with task details
    """
    lines = [
        f"ID: {task['id']}",
        f"Title: {task['title']}",
        f"Status: {task['status']}",
        f"Priority: {task['priority']}"
    ]

    if task.get('description'):
        lines.append(f"Description: {task['description']}")

    if task.get('due_date'):
        lines.append(f"Due Date: {task['due_date']}")

    lines.append(f"Created: {task['created_at']}")

    return '\n'.join(lines)
