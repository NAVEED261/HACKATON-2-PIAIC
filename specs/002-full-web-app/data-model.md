# Data Model: Phase 2 - Full Web App

**Feature**: Phase 2 - Full Web App
**Date**: 2025-12-07
**Database**: Neon PostgreSQL (serverless)
**ORM**: SQLAlchemy 2.0 (async)

## Overview

Phase 2 introduces multi-user support with three primary entities: **User**, **Task**, and **RefreshToken**. The Task entity preserves the 7-field schema from Phase 1 and adds `user_id` for data isolation and `updated_at` for optimistic locking.

**Migration from Phase 1**: The Phase 1 JSON file structure maps directly to the Task table schema, with the addition of `user_id` (foreign key) and `updated_at` (timestamp).

---

## Entity: User

**Purpose**: Represents an authenticated user with email/password credentials.

**Table Name**: `users`

### Fields

| Field Name     | Type            | Constraints                          | Description |
|----------------|-----------------|--------------------------------------|-------------|
| `id`           | INTEGER         | PRIMARY KEY, AUTO INCREMENT          | Unique user identifier |
| `email`        | VARCHAR(255)    | UNIQUE, NOT NULL                     | User's email address (used for login) |
| `password_hash`| VARCHAR(255)    | NOT NULL                             | bcrypt hashed password (10 salt rounds) |
| `display_name` | VARCHAR(100)    | NOT NULL                             | User's display name (shown in UI) |
| `created_at`   | TIMESTAMP       | NOT NULL, DEFAULT CURRENT_TIMESTAMP  | Account creation timestamp (UTC) |
| `updated_at`   | TIMESTAMP       | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP | Last profile update timestamp (UTC) |

### Validation Rules

- **email**: Must match RFC 5322 email format, max 255 characters
- **password** (plaintext, not stored): Minimum 8 characters, at least 1 uppercase, 1 lowercase, 1 digit (FR-008)
- **password_hash**: bcrypt hash with 10 salt rounds (FR-003)
- **display_name**: Required, 1-100 characters, no leading/trailing whitespace

### Indexes

```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at DESC);
```

**Rationale**:
- `email` unique index enforces one account per email and speeds up login queries
- `created_at` index supports admin analytics (user growth over time)

### Relationships

- **One-to-Many** with `tasks`: A user owns many tasks (`tasks.user_id → users.id`)
- **One-to-Many** with `refresh_tokens`: A user can have multiple active refresh tokens (`refresh_tokens.user_id → users.id`)

### SQLAlchemy Model Example

```python
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
```

---

## Entity: Task

**Purpose**: Represents a todo task owned by a user. Preserves Phase 1 schema with multi-user support.

**Table Name**: `tasks`

### Fields (Phase 1 Schema + Extensions)

| Field Name     | Type            | Constraints                          | Description |
|----------------|-----------------|--------------------------------------|-------------|
| `id`           | INTEGER         | PRIMARY KEY, AUTO INCREMENT          | Unique task identifier (Phase 1: sequential) |
| `title`        | VARCHAR(200)    | NOT NULL                             | Task title (max 200 chars, Phase 1 constraint) |
| `description`  | TEXT            | NULLABLE                             | Task description (max 1000 chars validated in app, Phase 1 constraint) |
| `status`       | VARCHAR(20)     | NOT NULL, DEFAULT 'pending'          | Task status: 'pending' or 'completed' (Phase 1 enum) |
| `priority`     | VARCHAR(10)     | NOT NULL, DEFAULT 'medium'           | Priority: 'low', 'medium', 'high' (Phase 1 enum) |
| `due_date`     | DATE            | NULLABLE                             | Optional due date in ISO 8601 format YYYY-MM-DD (Phase 1 format) |
| `created_at`   | TIMESTAMP       | NOT NULL, DEFAULT CURRENT_TIMESTAMP  | Task creation timestamp UTC (Phase 1 auto-generated) |
| **`user_id`**  | **INTEGER**     | **NOT NULL, FOREIGN KEY (users.id)** | **Phase 2 addition**: Owner of the task |
| **`updated_at`**| **TIMESTAMP**  | **NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP** | **Phase 2 addition**: Last modification timestamp |

### Validation Rules (Phase 1 Compatibility)

- **title**: Required, 1-200 characters (FR-009 Phase 2, inherited from Phase 1 data-model.md)
- **description**: Optional, max 1000 characters (Phase 1 constraint preserved)
- **status**: Enum ['pending', 'completed'] (Phase 1 values, validated in app)
- **priority**: Enum ['low', 'medium', 'high'], default 'medium' (Phase 1 values)
- **due_date**: Optional, must be ISO 8601 YYYY-MM-DD format, cannot be in the past (Phase 1 validator)
- **user_id**: Required, must reference existing user (enforced by foreign key)

### Indexes

```sql
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

**Rationale**:
- `user_id` index: Speeds up "list all tasks for user" queries (most common operation)
- `status` index: Supports filtering by status (FR-015)
- `created_at` index: Supports sorting by creation date
- `user_id + status` composite: Optimizes filtered queries (e.g., "show my pending tasks")
- `user_id + created_at` composite: Optimizes sorting user's tasks by date

### Relationships

- **Many-to-One** with `users`: A task belongs to one user (`tasks.user_id → users.id`)

### Foreign Key Constraints

```sql
ALTER TABLE tasks
ADD CONSTRAINT fk_tasks_user_id
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;
```

**ON DELETE CASCADE**: When a user is deleted, all their tasks are automatically deleted (data isolation compliance).

### SQLAlchemy Model Example

```python
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="pending", index=True)
    priority = Column(String(10), nullable=False, default="medium")
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="tasks")
```

### Phase 1 Migration Mapping

| Phase 1 JSON Field | Phase 2 Database Column | Notes |
|--------------------|-------------------------|-------|
| `id`               | `id`                    | Preserved as-is (auto-increment) |
| `title`            | `title`                 | Preserved as-is |
| `description`      | `description`           | Preserved as-is |
| `status`           | `status`                | Preserved as-is |
| `priority`         | `priority`              | Preserved as-is |
| `due_date`         | `due_date`              | Preserved as-is (ISO 8601 string → DATE) |
| `created_at`       | `created_at`            | Preserved as-is (ISO 8601 string → TIMESTAMP) |
| *(none)*           | `user_id`               | **NEW**: Assigned during migration (user must exist first) |
| *(none)*           | `updated_at`            | **NEW**: Set to `created_at` value during migration |

**Migration Script Location**: `scripts/migrate-phase1-data.py`

---

## Entity: RefreshToken

**Purpose**: Stores refresh tokens for JWT authentication, enabling secure session management and token rotation.

**Table Name**: `refresh_tokens`

### Fields

| Field Name     | Type            | Constraints                          | Description |
|----------------|-----------------|--------------------------------------|-------------|
| `id`           | INTEGER         | PRIMARY KEY, AUTO INCREMENT          | Unique token identifier |
| `user_id`      | INTEGER         | NOT NULL, FOREIGN KEY (users.id)     | Owner of the token |
| `token`        | VARCHAR(500)    | UNIQUE, NOT NULL                     | Hashed refresh token (SHA256) |
| `expires_at`   | TIMESTAMP       | NOT NULL                             | Token expiration time (7 days from creation, FR-006) |
| `created_at`   | TIMESTAMP       | NOT NULL, DEFAULT CURRENT_TIMESTAMP  | Token creation timestamp (UTC) |

### Validation Rules

- **token**: Must be unique, SHA256 hash of random 64-byte value
- **expires_at**: Must be > current time when validating
- **user_id**: Must reference existing user

### Indexes

```sql
CREATE UNIQUE INDEX idx_refresh_tokens_token ON refresh_tokens(token);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
```

**Rationale**:
- `token` unique index: Prevents token collisions, speeds up token lookup during refresh
- `user_id` index: Supports listing/revoking all user's tokens
- `expires_at` index: Enables efficient cleanup of expired tokens (cron job)

### Relationships

- **Many-to-One** with `users`: A refresh token belongs to one user (`refresh_tokens.user_id → users.id`)

### Foreign Key Constraints

```sql
ALTER TABLE refresh_tokens
ADD CONSTRAINT fk_refresh_tokens_user_id
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;
```

**ON DELETE CASCADE**: When a user is deleted, all their refresh tokens are invalidated.

### SQLAlchemy Model Example

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from db.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="refresh_tokens")
```

---

## Database Schema Diagram

```
┌─────────────────────────┐
│ users                   │
├─────────────────────────┤
│ id (PK)                 │
│ email (UNIQUE)          │
│ password_hash           │
│ display_name            │
│ created_at              │
│ updated_at              │
└─────────────────────────┘
         │ 1
         │
         │ 1:N
         ▼ N
┌─────────────────────────┐       ┌───────────────────────────┐
│ tasks                   │       │ refresh_tokens            │
├─────────────────────────┤       ├───────────────────────────┤
│ id (PK)                 │       │ id (PK)                   │
│ title                   │       │ user_id (FK → users.id)   │
│ description             │       │ token (UNIQUE)            │
│ status                  │       │ expires_at                │
│ priority                │       │ created_at                │
│ due_date                │       └───────────────────────────┘
│ created_at              │                 ▲ N
│ user_id (FK → users.id) │                 │
│ updated_at              │                 │ 1:N
└─────────────────────────┘                 │ 1
                                            │
                    (Same user relationship)
```

---

## Alembic Migration Strategy

### Initial Migration (Phase 2 Baseline)

**File**: `backend/src/db/migrations/versions/001_initial_schema.py`

**Operations**:
1. Create `users` table with all fields and indexes
2. Create `tasks` table with all fields and indexes
3. Create `refresh_tokens` table with all fields and indexes
4. Add foreign key constraints

### Future Migrations

- **002_add_task_tags.py**: If Phase 3 adds tagging feature
- **003_add_user_preferences.py**: If Phase 4 adds user settings
- Each migration must be reversible (`upgrade()` and `downgrade()` functions)

### Migration Execution

**Development**:
```bash
alembic upgrade head
```

**Production** (automated via Railway/Render):
```bash
alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000
```

---

## Data Isolation & Security

### Row-Level Security

**Application-Level Enforcement**:
- All task queries MUST filter by `user_id = current_user.id`
- FastAPI dependency injection ensures authenticated user context
- Example: `SELECT * FROM tasks WHERE user_id = $1 AND status = $2`

**No Database-Level RLS**: PostgreSQL Row-Level Security (RLS) policies are NOT used in Phase 2 to maintain simplicity. Application logic enforces data isolation.

### Audit Trail

**Phase 2 Approach**:
- `created_at` and `updated_at` timestamps provide basic audit trail
- No deletion tracking (hard deletes)
- Future phases may add `deleted_at` for soft deletes if required

---

## Performance Considerations

### Query Optimization

**Common Queries** (Expected p95 < 100ms):

1. **List user's tasks** (most frequent):
   ```sql
   SELECT * FROM tasks
   WHERE user_id = $1
   ORDER BY created_at DESC
   LIMIT 50;
   ```
   Optimized by: `idx_tasks_user_created` composite index

2. **Filter by status**:
   ```sql
   SELECT * FROM tasks
   WHERE user_id = $1 AND status = $2
   ORDER BY created_at DESC;
   ```
   Optimized by: `idx_tasks_user_status` composite index

3. **Authenticate user**:
   ```sql
   SELECT * FROM users WHERE email = $1;
   ```
   Optimized by: `idx_users_email` unique index

### Connection Pooling

**SQLAlchemy Configuration** (from research.md):
- Pool size: 5 connections (Neon free tier limit: 1 concurrent)
- Max overflow: 10
- Pool timeout: 30 seconds
- Pool recycle: 3600 seconds (1 hour, Neon connection timeout)

---

## Testing Strategy

### Test Database

**Setup**: In-memory SQLite for unit/integration tests
**Rationale**: Fast, isolated, no external dependencies

**Pytest Fixture** (`tests/conftest.py`):
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base

@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
```

### Test Data Factories

Use **factory-boy** or manual factories for test data:

```python
def create_test_user(db, email="test@example.com"):
    user = User(
        email=email,
        password_hash=bcrypt_hash("TestPassword123"),
        display_name="Test User"
    )
    db.add(user)
    db.commit()
    return user

def create_test_task(db, user_id, title="Test Task"):
    task = Task(
        user_id=user_id,
        title=title,
        status="pending",
        priority="medium"
    )
    db.add(task)
    db.commit()
    return task
```

---

## Migration from Phase 1

### Migration Script Requirements

**Script**: `scripts/migrate-phase1-data.py`

**Input**: Phase 1 `tasks.json` file
**Output**: PostgreSQL database with migrated tasks

**Process**:
1. Create a default user for Phase 1 data migration
2. Read `tasks.json` (Phase 1 format)
3. For each task in JSON:
   - Map all 7 Phase 1 fields to Task model
   - Add `user_id` (reference to default user)
   - Set `updated_at` = `created_at`
   - Insert into `tasks` table
4. Verify: All Phase 1 regression tests pass with migrated data

**Example Migration Logic**:
```python
import json
from sqlalchemy.orm import Session
from models.user import User
from models.task import Task

def migrate_phase1_data(json_path: str, db: Session):
    # Create default migration user
    migration_user = User(
        email="phase1-migration@example.com",
        password_hash="<disabled>",  # No login allowed
        display_name="Phase 1 Migration"
    )
    db.add(migration_user)
    db.commit()

    # Read Phase 1 JSON
    with open(json_path) as f:
        tasks_data = json.load(f)

    # Migrate tasks
    for task_json in tasks_data:
        task = Task(
            id=task_json["id"],  # Preserve original IDs
            title=task_json["title"],
            description=task_json.get("description"),
            status=task_json["status"],
            priority=task_json["priority"],
            due_date=task_json.get("due_date"),
            created_at=task_json["created_at"],
            updated_at=task_json["created_at"],  # No updates yet
            user_id=migration_user.id
        )
        db.add(task)

    db.commit()
    print(f"Migrated {len(tasks_data)} tasks from Phase 1")
```

---

**Data Model Complete**: 2025-12-07
**Next Step**: Generate API contracts (`contracts/api-endpoints.md`, `contracts/openapi.yaml`)
