"""JSON file storage module with atomic writes

Implements load_tasks and save_tasks functions for tasks.json persistence.
Uses atomic write pattern (temp file + rename) to prevent corruption.
"""

import json
import sys
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict


DEFAULT_STORAGE_FILE = 'tasks.json'


def load_tasks(file_path: str = DEFAULT_STORAGE_FILE) -> List[Dict]:
    """Load tasks from JSON file

    Args:
        file_path: Path to tasks JSON file (default: tasks.json)

    Returns:
        List of task dictionaries

    Exits:
        Exit code 2 on JSON corruption with recovery instructions
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
            return tasks
    except FileNotFoundError:
        # First run or file deleted - start fresh
        return []
    except json.JSONDecodeError:
        # Corrupted file - do not auto-delete, preserve data
        print(f"Error: {file_path} is corrupted.", file=sys.stderr)
        print(f"Backup the file and delete it to reset, or manually fix JSON syntax.", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        sys.exit(2)


def save_tasks(tasks: List[Dict], file_path: str = DEFAULT_STORAGE_FILE) -> None:
    """Save tasks to JSON file using atomic writes

    Uses temp file + rename pattern to prevent corruption from interrupted writes.

    Args:
        tasks: List of task dictionaries
        file_path: Path to tasks JSON file (default: tasks.json)

    Exits:
        Exit code 2 on write failure
    """
    try:
        # Get directory of target file for temp file placement
        file_dir = Path(file_path).parent or Path('.')

        # Create temporary file in same directory as target
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            delete=False,
            dir=file_dir,
            suffix='.tmp'
        ) as tmp:
            json.dump(tasks, tmp, indent=2, ensure_ascii=False)
            tmp_path = tmp.name

        # Atomic rename - replaces existing file
        shutil.move(tmp_path, file_path)

    except Exception as e:
        print(f"Error saving tasks to {file_path}: {e}", file=sys.stderr)
        # Clean up temp file if it exists
        try:
            Path(tmp_path).unlink()
        except:
            pass
        sys.exit(2)
