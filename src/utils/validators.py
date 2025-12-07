"""Input validation utilities for Task entity fields

Implements validation rules from data-model.md
"""

from datetime import datetime
from typing import Optional


# Valid priority levels (FR-015)
VALID_PRIORITIES = {'low', 'medium', 'high'}

# Valid status values
VALID_STATUSES = {'pending', 'completed'}


def validate_title(title: str) -> bool:
    """Validate task title is not empty (FR-001)

    Args:
        title: Task title string

    Returns:
        True if title is non-empty and not whitespace-only, False otherwise
    """
    return bool(title and title.strip())


def validate_date(date_str: str) -> bool:
    """Validate date string matches ISO 8601 format (YYYY-MM-DD)

    Args:
        date_str: Date string to validate

    Returns:
        True if date is valid and matches format, False otherwise
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_priority(priority: str) -> bool:
    """Validate priority level (FR-015)

    Args:
        priority: Priority level string

    Returns:
        True if priority is "low", "medium", or "high", False otherwise
    """
    return priority in VALID_PRIORITIES


def validate_status(status: str) -> bool:
    """Validate task status

    Args:
        status: Status string

    Returns:
        True if status is "pending" or "completed", False otherwise
    """
    return status in VALID_STATUSES


def validate_title_length(title: str, max_length: int = 200) -> bool:
    """Validate title does not exceed maximum length

    Args:
        title: Task title string
        max_length: Maximum allowed characters (default: 200)

    Returns:
        True if title length is within limit, False otherwise
    """
    return len(title) <= max_length


def validate_description_length(description: Optional[str], max_length: int = 1000) -> bool:
    """Validate description does not exceed maximum length

    Args:
        description: Task description string (can be None)
        max_length: Maximum allowed characters (default: 1000)

    Returns:
        True if description is None or within limit, False otherwise
    """
    if description is None:
        return True
    return len(description) <= max_length
