# Quickstart Guide: Phase 1 - Console Todo App

**Last Updated**: 2025-12-06
**Version**: 1.0.0 (Phase 1)

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Commands Reference](#commands-reference)
4. [Common Workflows](#common-workflows)
5. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites

- Python 3.11 or higher
- Terminal/Command Prompt access

### Verify Python Version

```bash
python --version
# Should show: Python 3.11.x or higher
```

### Install Todo CLI

```bash
# Clone the repository (update with actual repo URL)
git clone <repository-url>
cd hackaton-2

# No dependencies to install (uses Python stdlib only)
# Make the CLI executable (optional)
chmod +x src/todo_cli.py  # macOS/Linux only
```

### Run the CLI

```bash
# Option 1: Direct Python execution
python src/todo_cli.py --help

# Option 2: Create alias for convenience (optional)
alias todo="python /path/to/hackaton-2/src/todo_cli.py"
```

---

## Basic Usage

### Your First Task

```bash
# Add your first task
todo add "Buy groceries"
# Output: Task added successfully! ID: 1

# View all tasks
todo list
# Output:
# ID    Title                Status      Priority    Due Date
# --------------------------------------------------------------
# 1     Buy groceries        pending     medium      N/A
```

### Mark Task Complete

```bash
todo complete 1
# Output: Task #1 marked as completed!

# Verify it's completed
todo list
# Output:
# ID    Title                Status      Priority    Due Date
# --------------------------------------------------------------
# 1     Buy groceries        completed   medium      N/A
```

---

## Commands Reference

### 1. Add a Task

#### Simple Task

```bash
todo add "Call dentist"
```

#### Task with Description

```bash
todo add "Submit report" --description "Q4 financial analysis"
```

#### Task with Due Date

```bash
todo add "Team meeting" --due-date 2025-12-15
```

#### Task with Priority

```bash
todo add "Fix production bug" --priority high
```

#### Complete Task (All Options)

```bash
todo add "Client presentation" \
  --description "Quarterly business review slides" \
  --due-date 2025-12-20 \
  --priority high
```

---

### 2. List Tasks

#### All Tasks

```bash
todo list
```

#### Pending Tasks Only

```bash
todo list --status pending
```

#### Completed Tasks Only

```bash
todo list --status completed
```

#### High Priority Tasks

```bash
todo list --priority high
```

#### Combined Filters

```bash
todo list --status pending --priority high
```

#### Sort by Due Date

```bash
todo list --sort-by due_date
```

---

### 3. Complete a Task

```bash
# Replace <id> with the task ID from 'todo list'
todo complete <id>

# Example
todo complete 5
```

---

### 4. Update a Task

#### Change Title

```bash
todo update 2 --title "New task title"
```

#### Change Description

```bash
todo update 2 --description "Updated description"
```

#### Change Due Date

```bash
todo update 2 --due-date 2025-12-31
```

#### Change Priority

```bash
todo update 2 --priority high
```

#### Undo Completion (Mark as Pending)

```bash
todo update 3 --status pending
```

#### Update Multiple Fields

```bash
todo update 5 \
  --title "Revised title" \
  --priority high \
  --due-date 2025-12-25
```

---

### 5. Delete a Task

#### With Confirmation Prompt

```bash
todo delete 5
# Prompt: Are you sure you want to delete task #5: "Task title"? (y/N):
# Enter 'y' to confirm or 'n' to cancel
```

#### Without Confirmation

```bash
todo delete 5 --confirm
```

---

## Common Workflows

### Daily Task Management

```bash
# Morning: Review pending tasks
todo list --status pending

# Add today's tasks
todo add "Review pull requests" --priority high
todo add "Update documentation" --priority medium
todo add "Team standup at 10am" --due-date 2025-12-06

# Throughout the day: Complete tasks
todo complete 1
todo complete 3

# Evening: Check what's left
todo list --status pending
```

---

### Weekly Planning

```bash
# Monday: Add week's tasks with due dates
todo add "Prepare Monday presentation" --due-date 2025-12-06 --priority high
todo add "Code review session" --due-date 2025-12-07
todo add "Sprint planning" --due-date 2025-12-08 --priority high
todo add "Deploy to staging" --due-date 2025-12-09
todo add "Weekly report" --due-date 2025-12-10

# View tasks sorted by due date
todo list --sort-by due_date

# Friday: Review completed vs pending
todo list --status completed
todo list --status pending
```

---

### Project-Based Organization

**Tip**: Create separate directories for different projects, each with its own `tasks.json`

```bash
# Project A
cd ~/projects/project-a
todo add "Implement user authentication"
todo add "Write API tests"

# Project B
cd ~/projects/project-b
todo add "Fix database migration"
todo add "Update dependencies"

# Each directory maintains its own task list
```

---

### Urgent Task Prioritization

```bash
# Add urgent task
todo add "URGENT: Production hotfix" --priority high --due-date 2025-12-06

# View only high-priority tasks
todo list --priority high

# Complete urgent task
todo complete <id>
```

---

## Troubleshooting

### Error: "Title cannot be empty"

**Cause**: You tried to add a task without a title or with an empty string

**Solution**:
```bash
# Wrong
todo add ""

# Correct
todo add "My task title"
```

---

### Error: "Invalid date format. Use YYYY-MM-DD"

**Cause**: Due date is not in ISO 8601 format

**Solution**:
```bash
# Wrong
todo add "Task" --due-date 12/31/2025

# Correct
todo add "Task" --due-date 2025-12-31
```

---

### Error: "Task with ID X not found"

**Cause**: You referenced a task ID that doesn't exist (deleted or never created)

**Solution**:
```bash
# List all tasks to see valid IDs
todo list

# Use a valid ID from the list
todo complete <valid_id>
```

---

### Error: "tasks.json is corrupted"

**Cause**: JSON file has invalid syntax (manual edit gone wrong)

**Solution**:
```bash
# Option 1: Backup and reset
cp tasks.json tasks.backup.json
rm tasks.json
# CLI will create a fresh tasks.json

# Option 2: Manually fix JSON syntax
# Open tasks.json in a text editor and fix syntax errors
# Validate JSON at https://jsonlint.com/
```

---

### Error: "Permission denied"

**Cause**: No write access to current directory

**Solution**:
```bash
# Check directory permissions
ls -la tasks.json

# Fix permissions (macOS/Linux)
chmod 644 tasks.json

# Windows: Right-click tasks.json → Properties → Security → Edit permissions
```

---

### Tasks Not Showing Up

**Issue**: Added tasks but `todo list` shows "No tasks found"

**Cause**: Multiple `tasks.json` files in different directories

**Solution**:
```bash
# Check which directory you're in
pwd

# Find all tasks.json files
find ~ -name tasks.json  # macOS/Linux
dir tasks.json /s        # Windows

# Consolidate to one location or use project-specific directories
```

---

### CLI Not Found

**Issue**: `todo: command not found`

**Solution**:
```bash
# Use full Python path
python src/todo_cli.py --help

# Or create a shell alias
echo "alias todo='python /full/path/to/src/todo_cli.py'" >> ~/.bashrc
source ~/.bashrc  # Reload shell config
```

---

## Data Storage

### Where Are My Tasks Stored?

- **File**: `tasks.json` in your current working directory
- **Format**: JSON array of task objects
- **Backup**: Copy `tasks.json` to back up your tasks

### Manual Backup

```bash
# Create backup
cp tasks.json tasks_backup_$(date +%Y%m%d).json

# Restore from backup
cp tasks_backup_20251206.json tasks.json
```

---

## Tips & Best Practices

### Use Quotes for Multi-Word Titles

```bash
# Wrong
todo add Buy groceries and cook dinner

# Correct
todo add "Buy groceries and cook dinner"
```

### Check Task List Before Deleting

```bash
# Always list tasks first to verify ID
todo list
# Then delete
todo delete 5 --confirm
```

### Use Priority Levels Consistently

- **High**: Urgent, deadline-driven, blockers
- **Medium**: Normal workflow tasks (default)
- **Low**: Nice-to-have, low urgency

### Set Due Dates for Time-Sensitive Tasks

```bash
# Good practice for deadline-driven work
todo add "Submit tax documents" --due-date 2025-12-15 --priority high
```

### Review Completed Tasks Periodically

```bash
# Weekly review of accomplishments
todo list --status completed
```

---

## Next Steps

### Phase 1 ✅ (Current)
- CLI task management
- JSON file storage
- Local, offline operation

### Phase 2 (Coming Soon)
- Web-based UI (Next.js)
- REST API (FastAPI)
- PostgreSQL database
- User authentication
- Multi-device sync

### Phase 3 (Future)
- AI chatbot interface
- Natural language task creation
- Smart task suggestions

---

## Getting Help

### Built-in Help

```bash
# General help
todo --help

# Command-specific help
todo add --help
todo list --help
todo complete --help
todo update --help
todo delete --help
```

### Report Issues

- GitHub Issues: [repository-url]/issues
- Documentation: [repository-url]/docs

---

## Version History

- **v1.0.0** (2025-12-06): Initial Phase 1 release - Console Todo App
