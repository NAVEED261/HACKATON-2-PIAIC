# Data Model: Phase 1 - Console Todo App

**Date**: 2025-12-06
**Feature**: 001-phase1-console-todo
**Purpose**: Define Task entity schema, validation rules, and state transitions

## Entity: Task

### Schema

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| id | Integer | Yes | Auto-increment | Unique, sequential starting from 1 |
| title | String | Yes | - | Non-empty, max 200 characters |
| description | String | No | null | Max 1000 characters |
| status | String (Enum) | Yes | "pending" | One of: "pending", "completed" |
| priority | String (Enum) | Yes | "medium" | One of: "low", "medium", "high" |
| due_date | String (ISO 8601) | No | null | Format: YYYY-MM-DD, must be valid date |
| created_at | String (ISO 8601) | Yes | Current timestamp | Format: YYYY-MM-DDTHH:MM:SS |

### JSON Representation

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, and coffee",
  "status": "pending",
  "priority": "medium",
  "due_date": "2025-12-08",
  "created_at": "2025-12-06T10:30:00"
}
```

### Minimal Task Example

```json
{
  "id": 2,
  "title": "Call dentist",
  "description": null,
  "status": "pending",
  "priority": "medium",
  "due_date": null,
  "created_at": "2025-12-06T14:15:00"
}
```

## Validation Rules

### FR-001: Add Task - Title Required
- **Rule**: `title` field MUST NOT be empty or whitespace-only
- **Error**: "Title cannot be empty"
- **Implementation**:
  ```python
  def validate_title(title: str) -> bool:
      return bool(title and title.strip())
  ```

### FR-002: Unique ID Assignment
- **Rule**: Each task MUST have a unique integer ID
- **Implementation**: Track highest ID, increment by 1
  ```python
  def get_next_id(tasks: list) -> int:
      if not tasks:
          return 1
      return max(task['id'] for task in tasks) + 1
  ```

### FR-003: Optional Fields Validation
- **description**: If provided, max 1000 characters
- **due_date**: If provided, must match YYYY-MM-DD format and be valid date
- **priority**: If provided, must be one of: "low", "medium", "high"

### FR-015: Priority Levels
- **Rule**: Priority MUST be one of three values
- **Valid Values**: "low", "medium", "high"
- **Default**: "medium"
- **Error**: "Priority must be low, medium, or high"
- **Implementation**:
  ```python
  VALID_PRIORITIES = {'low', 'medium', 'high'}

  def validate_priority(priority: str) -> bool:
      return priority in VALID_PRIORITIES
  ```

### Date Format Validation
- **Rule**: Dates MUST follow ISO 8601 (YYYY-MM-DD)
- **Error**: "Invalid date format. Use YYYY-MM-DD"
- **Implementation**:
  ```python
  from datetime import datetime

  def validate_date(date_str: str) -> bool:
      try:
          datetime.strptime(date_str, '%Y-%m-%d')
          return True
      except ValueError:
          return False
  ```

### Timestamp Generation
- **created_at**: Automatically set to current UTC time on task creation
- **Format**: ISO 8601 with time (YYYY-MM-DDTHH:MM:SS)
- **Implementation**:
  ```python
  from datetime import datetime

  def get_current_timestamp() -> str:
      return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
  ```

## State Transitions

### Status State Machine

```
┌─────────┐
│ pending │ ◄─── Initial state (all new tasks)
└─────────┘
     │
     │ complete <task_id>
     ▼
┌───────────┐
│ completed │
└───────────┘
```

**Allowed Transitions**:
- **pending → completed**: Via `todo complete <id>` command
- **completed → pending**: Via `todo update <id> --status pending` command (undo completion)

**Business Rules**:
- Tasks are created in "pending" status by default
- No intermediate states (only 2 states for Phase 1 simplicity)
- Status can be toggled back and forth (no irreversible transitions)

## Entity Relationships

### Phase 1: No Relationships
- Single-user application
- No user entity (deferred to Phase 2)
- No task categories or tags
- No task dependencies or subtasks

### Phase 2 Migration: Planned Relationships
```
User 1──────* Task
(one user has many tasks)

Fields to add in Phase 2:
- Task.user_id: Foreign key to User.id
- Task.updated_at: Track last modification time
```

## Storage Format

### JSON File Structure

**File**: `tasks.json` (in current working directory)

**Format**: Array of task objects

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "pending",
    "priority": "high",
    "due_date": "2025-12-08",
    "created_at": "2025-12-06T10:00:00"
  },
  {
    "id": 2,
    "title": "Call dentist",
    "description": null,
    "status": "pending",
    "priority": "medium",
    "due_date": null,
    "created_at": "2025-12-06T11:30:00"
  },
  {
    "id": 3,
    "title": "Submit report",
    "description": "Q4 financial analysis",
    "status": "completed",
    "priority": "high",
    "due_date": "2025-12-05",
    "created_at": "2025-12-01T09:00:00"
  }
]
```

### Empty State

**First Run**: File does not exist
**After First Task**: `[]` or array with one task

## Data Integrity Rules

### FR-012: Prevent Duplicate IDs
- **Enforcement**: ID assignment logic ensures uniqueness
- **Check**: Before adding task, verify ID not in use
  ```python
  existing_ids = {task['id'] for task in tasks}
  if new_id in existing_ids:
      # This should never happen with sequential IDs
      raise ValueError(f"Duplicate ID {new_id}")
  ```

### FR-004: Data Persistence
- **Guarantee**: All operations write to `tasks.json` immediately
- **Atomic Writes**: Use temp file + rename to prevent corruption
- **Backup**: Optional auto-backup before destructive operations (delete, update)

### FR-014: Corrupted Storage Handling
- **Detection**: Catch `json.JSONDecodeError` on file read
- **Recovery**:
  1. Print error message with file path
  2. Suggest backup and reset
  3. Do not auto-delete (preserve user data)

```python
try:
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
except json.JSONDecodeError:
    print("Error: tasks.json is corrupted.")
    print("Backup the file and delete it to reset, or manually fix JSON syntax.")
    sys.exit(2)
except FileNotFoundError:
    tasks = []  # First run, start fresh
```

## Edge Cases

### Empty Title
- **Input**: `todo add ""`
- **Validation**: Reject with error "Title cannot be empty"

### Very Long Title (>200 characters)
- **Validation**: Truncate or reject with error
- **Recommendation**: Reject with "Title must be 200 characters or less"

### Invalid Date Format
- **Input**: `todo add "Task" --due-date 12/06/2025`
- **Validation**: Reject with "Invalid date format. Use YYYY-MM-DD"

### Invalid Task ID
- **Input**: `todo complete 999` (task doesn't exist)
- **Validation**: Error "Task with ID 999 not found"

### Non-Numeric Task ID
- **Input**: `todo complete abc`
- **Validation**: argparse type validation catches this: "argument id: invalid int value: 'abc'"

### Missing Storage File
- **Scenario**: First run or user deleted `tasks.json`
- **Handling**: Create empty array `[]`, no error

### Concurrent Access
- **Phase 1 Assumption**: Single-user, no concurrent access
- **Phase 2**: Database handles concurrency with locks

## Schema Evolution (Phase 2 Preview)

### Phase 1 → Phase 2 Migration

**PostgreSQL Schema**:
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority VARCHAR(10) NOT NULL DEFAULT 'medium',
    due_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

**Field Mapping**:
- ✅ All Phase 1 fields map directly to PostgreSQL columns
- ✅ `id` → SERIAL (auto-increment)
- ✅ `created_at` → TIMESTAMP
- ➕ New: `user_id` (multi-user support)
- ➕ New: `updated_at` (track modifications)

**Migration Script**: Convert `tasks.json` → PostgreSQL INSERT statements
