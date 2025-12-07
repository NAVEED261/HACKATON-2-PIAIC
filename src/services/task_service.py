"""Task service - Business logic for CRUD operations

Implements task management functions: create, read, update, delete, filter
"""

from typing import List, Dict, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add src to path for absolute imports when run as script
if __name__ == '__main__' or __package__ is None:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.validators import (
    validate_title,
    validate_date,
    validate_priority,
    validate_status,
    validate_title_length,
    validate_description_length
)
from services.storage import load_tasks, save_tasks


def get_next_id(tasks: List[Dict]) -> int:
    """Generate next sequential ID for new task (FR-002)

    Args:
        tasks: List of existing task dictionaries

    Returns:
        Next available ID (starts from 1)
    """
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1


def create_task(
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None
) -> Dict:
    """Create a new task dictionary with validation

    Args:
        title: Task title (required)
        description: Task description (optional)
        priority: Priority level (default: medium)
        due_date: Due date in YYYY-MM-DD format (optional)

    Returns:
        Task dictionary with all 7 fields

    Raises:
        ValueError: If validation fails
    """
    # Validate title
    if not validate_title(title):
        raise ValueError("Title cannot be empty")

    if not validate_title_length(title):
        raise ValueError("Title must be 200 characters or less")

    # Validate description
    if description and not validate_description_length(description):
        raise ValueError("Description must be 1000 characters or less")

    # Validate priority
    if not validate_priority(priority):
        raise ValueError(f"Priority must be one of: low, medium, high")

    # Validate due date
    if due_date and not validate_date(due_date):
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

    # Load existing tasks to get next ID
    tasks = load_tasks()
    next_id = get_next_id(tasks)

    # Generate timestamp
    created_at = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    # Create task dictionary
    task = {
        'id': next_id,
        'title': title,
        'description': description,
        'status': 'pending',
        'priority': priority,
        'due_date': due_date,
        'created_at': created_at
    }

    return task


def get_all_tasks() -> List[Dict]:
    """Get all tasks from storage

    Returns:
        List of all task dictionaries
    """
    return load_tasks()


def get_task_by_id(task_id: int) -> Optional[Dict]:
    """Find task by ID

    Args:
        task_id: Task ID to find

    Returns:
        Task dictionary if found, None otherwise
    """
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None


def add_task(
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None
) -> Dict:
    """Add a new task to storage

    Args:
        title: Task title (required)
        description: Task description (optional)
        priority: Priority level (default: medium)
        due_date: Due date in YYYY-MM-DD format (optional)

    Returns:
        Created task dictionary

    Raises:
        ValueError: If validation fails
    """
    # Create task with validation
    task = create_task(title, description, priority, due_date)

    # Load, append, save
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    return task


def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None
) -> List[Dict]:
    """List tasks with optional filtering

    Args:
        status: Filter by status (optional)
        priority: Filter by priority (optional)

    Returns:
        List of filtered task dictionaries
    """
    tasks = load_tasks()

    # Apply filters
    if status and status != 'all':
        tasks = [t for t in tasks if t['status'] == status]

    if priority:
        tasks = [t for t in tasks if t['priority'] == priority]

    return tasks


def complete_task(task_id: int) -> Dict:
    """Mark task as completed

    Args:
        task_id: ID of task to complete

    Returns:
        Updated task dictionary

    Raises:
        ValueError: If task not found
    """
    tasks = load_tasks()

    # Find task
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break

    if not task:
        raise ValueError(f"Task with ID {task_id} not found")

    # Update status
    task['status'] = 'completed'
    save_tasks(tasks)

    return task


def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    due_date: Optional[str] = None
) -> Dict:
    """Update task fields

    Args:
        task_id: ID of task to update
        title: New title (optional)
        description: New description (optional)
        priority: New priority (optional)
        status: New status (optional)
        due_date: New due date (optional)

    Returns:
        Updated task dictionary

    Raises:
        ValueError: If task not found or validation fails
    """
    tasks = load_tasks()

    # Find task
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break

    if not task:
        raise ValueError(f"Task with ID {task_id} not found")

    # Check at least one field provided
    if not any([title, description is not None, priority, status, due_date is not None]):
        raise ValueError("At least one field must be specified to update")

    # Validate and update fields
    if title is not None:
        if not validate_title(title):
            raise ValueError("Title cannot be empty")
        if not validate_title_length(title):
            raise ValueError("Title must be 200 characters or less")
        task['title'] = title

    if description is not None:
        if not validate_description_length(description):
            raise ValueError("Description must be 1000 characters or less")
        task['description'] = description

    if priority is not None:
        if not validate_priority(priority):
            raise ValueError("Priority must be one of: low, medium, high")
        task['priority'] = priority

    if status is not None:
        if not validate_status(status):
            raise ValueError("Status must be one of: pending, completed")
        task['status'] = status

    if due_date is not None:
        if due_date and not validate_date(due_date):
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        task['due_date'] = due_date

    save_tasks(tasks)
    return task


def delete_task(task_id: int) -> Dict:
    """Delete task by ID

    Args:
        task_id: ID of task to delete

    Returns:
        Deleted task dictionary

    Raises:
        ValueError: If task not found
    """
    tasks = load_tasks()

    # Find and remove task
    task = None
    for i, t in enumerate(tasks):
        if t['id'] == task_id:
            task = tasks.pop(i)
            break

    if not task:
        raise ValueError(f"Task with ID {task_id} not found")

    save_tasks(tasks)
    return task


def filter_tasks(
    tasks: List[Dict],
    status: Optional[str] = None,
    priority: Optional[str] = None
) -> List[Dict]:
    """Filter tasks by status and/or priority

    Args:
        tasks: List of task dictionaries
        status: Filter by status (optional)
        priority: Filter by priority (optional)

    Returns:
        Filtered list of task dictionaries
    """
    filtered = tasks

    if status and status != 'all':
        filtered = [t for t in filtered if t['status'] == status]

    if priority:
        filtered = [t for t in filtered if t['priority'] == priority]

    return filtered
