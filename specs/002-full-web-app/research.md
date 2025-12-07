# Phase 2 Technology Research: Full Web Application

**Phase**: 002-full-web-app
**Status**: Research Complete
**Created**: 2025-12-07
**Purpose**: Document technology decisions and best practices for migrating from Phase 1 CLI to full-stack web application

---

## Table of Contents

1. [Next.js 14+ Best Practices](#nextjs-14-best-practices)
2. [FastAPI Best Practices](#fastapi-best-practices)
3. [JWT Authentication Implementation](#jwt-authentication-implementation)
4. [Neon PostgreSQL Integration](#neon-postgresql-integration)
5. [SendGrid Email Integration](#sendgrid-email-integration)
6. [Frontend-Backend Communication](#frontend-backend-communication)
7. [Testing Strategies](#testing-strategies)
8. [Deployment Considerations](#deployment-considerations)

---

## Next.js 14+ Best Practices

### App Router vs Pages Router

**Decision**: Use App Router (Next.js 13+)

**Rationale**:
- App Router is the future of Next.js and provides better performance through React Server Components
- Simplified data fetching with native async/await in components
- Better code organization with colocation of routes, layouts, and components
- Streaming and Suspense support out of the box
- Aligns with React 18+ features and future roadmap

**Alternatives Considered**:
- Pages Router: Legacy approach, still supported but not recommended for new projects
- Remix: Similar philosophy but smaller ecosystem and less corporate backing

**Implementation Notes**:
- Use `app/` directory structure instead of `pages/`
- Define routes using folder structure: `app/dashboard/page.tsx`
- Use `layout.tsx` for shared UI across route segments
- Use `loading.tsx` for loading states (automatic Suspense boundaries)
- Use `error.tsx` for error boundaries
- Server Components by default, Client Components only when needed (interactive state, browser APIs, event listeners)

**Project Structure**:
```
app/
├── (auth)/
│   ├── login/
│   │   └── page.tsx
│   ├── register/
│   │   └── page.tsx
│   └── layout.tsx          # Auth-specific layout
├── (dashboard)/
│   ├── tasks/
│   │   └── page.tsx
│   └── layout.tsx          # Dashboard layout with nav
├── api/                     # API routes (if needed for BFF pattern)
│   └── auth/
│       └── route.ts
├── layout.tsx              # Root layout
└── page.tsx                # Home page
```

**Gotchas to Avoid**:
- Don't use `'use client'` everywhere - only for interactive components
- Server Components cannot use React hooks (useState, useEffect, etc.)
- Client Components cannot be async functions
- Avoid over-nesting route groups - keep structure flat

---

### Server Components vs Client Components

**Decision**: Server Components by default, Client Components only when necessary

**Rationale**:
- Server Components reduce JavaScript bundle size (zero client-side JS for non-interactive components)
- Better performance through server-side rendering and streaming
- Direct database/API access without exposing credentials
- Automatic code splitting and optimization

**When to Use Server Components**:
- Static content (headers, footers, layouts)
- Data fetching from databases or APIs
- Token validation and authentication checks
- Markdown rendering, syntax highlighting

**When to Use Client Components** (add `'use client'` directive):
- Interactive elements (buttons with onClick, forms with onChange)
- React hooks (useState, useEffect, useContext)
- Browser APIs (localStorage, window, document)
- Event listeners
- Third-party libraries that depend on browser APIs

**Implementation Notes**:
- Server Components can import Client Components, but not vice versa
- Pass data from Server to Client Components via props
- Use Server Actions for form submissions (no need for API routes)
- Client Components should be as small as possible (extract server logic into parent)

**Example Pattern**:
```tsx
// app/tasks/page.tsx (Server Component)
import { TaskList } from '@/components/TaskList';
import { getTasks } from '@/lib/tasks';

export default async function TasksPage() {
  const tasks = await getTasks(); // Direct DB access
  return <TaskList tasks={tasks} />; // Pass data to client
}

// components/TaskList.tsx (Client Component)
'use client';
import { useState } from 'react';

export function TaskList({ tasks }) {
  const [filter, setFilter] = useState('all');
  // Interactive filtering logic
}
```

**Gotchas to Avoid**:
- Don't fetch data in Client Components when you can do it in Server Components
- Don't pass functions or non-serializable objects from Server to Client Components
- Don't use Server Components inside Client Components (composition pattern instead)

---

### State Management Strategy

**Decision**: Use React Context API + Server State from Server Components

**Rationale**:
- Simplicity principle: avoid external dependencies unless necessary
- Server Components eliminate most client-side state needs
- Context API sufficient for authentication state and UI preferences
- Avoid over-engineering with Redux/Zustand for Phase 2 scope

**Alternatives Considered**:
- Redux Toolkit: Overkill for Phase 2, adds complexity and bundle size
- Zustand: Lightweight but unnecessary when most state lives on server
- Jotai/Recoil: Atomic state management, good for complex apps but premature for Phase 2

**Implementation Notes**:
- Create `AuthContext` for user authentication state
- Create `ThemeContext` for dark mode preference (if needed)
- Use Server Components for task data (fetch on each request/navigation)
- Use URL state for filters and pagination (`searchParams`)
- Consider SWR or React Query only if Phase 3 needs real-time updates

**Context Pattern**:
```tsx
// context/AuthContext.tsx
'use client';
import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check for existing session on mount
    checkAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

**URL State Pattern** (preferred for filters):
```tsx
// app/tasks/page.tsx
export default function TasksPage({ searchParams }) {
  const status = searchParams.status || 'all';
  const priority = searchParams.priority || 'all';

  // Use searchParams for filtering - shareable URLs, no client state
}
```

**Gotchas to Avoid**:
- Don't store task data in Context - fetch from server on each navigation
- Don't use Context for data that should be in URL (breaks shareable links)
- Don't create too many contexts - keep it minimal (auth + theme max)

---

### TailwindCSS Integration

**Decision**: Use TailwindCSS with default configuration + shadcn/ui component library

**Rationale**:
- Utility-first CSS reduces CSS bundle size and eliminates naming conflicts
- Next.js has first-class Tailwind support (zero config)
- shadcn/ui provides accessible, customizable components without framework lock-in
- Aligns with rapid development goals for Phase 2

**Alternatives Considered**:
- CSS Modules: More verbose, requires separate CSS files
- Styled Components: Runtime CSS-in-JS has performance overhead
- Material UI: Heavy framework, harder to customize, larger bundle size

**Implementation Notes**:
- Install Tailwind during Next.js setup: `npx create-next-app@latest --tailwind`
- Use shadcn/ui for complex components: `npx shadcn-ui@latest init`
- Install components as needed: `npx shadcn-ui@latest add button card form`
- Customize theme in `tailwind.config.ts` (colors, spacing)
- Use Tailwind's dark mode with `class` strategy

**Configuration**:
```ts
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class',
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          // ... color scale
          900: '#0c4a6e',
        },
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
};

export default config;
```

**Component Pattern with shadcn/ui**:
```tsx
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

export function TaskCard({ task }) {
  return (
    <Card className="p-6 hover:shadow-lg transition-shadow">
      <h3 className="text-lg font-semibold">{task.title}</h3>
      <Button variant="outline" size="sm">Complete</Button>
    </Card>
  );
}
```

**Gotchas to Avoid**:
- Don't mix Tailwind with other CSS frameworks (conflicts)
- Don't use `@apply` excessively - defeats the purpose of utility classes
- Don't forget to configure content paths for tree-shaking
- Don't hardcode colors - use theme variables for consistency

---

## FastAPI Best Practices

### Project Structure for Scalable APIs

**Decision**: Use layered architecture with separation of concerns

**Rationale**:
- Clear separation between API routes, business logic, and data access
- Easy to test each layer independently
- Aligns with Phase 1's task_service.py pattern
- Scales well when Phase 3 adds AI features

**Project Structure**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Environment variables, settings
│   ├── dependencies.py         # Shared dependencies (auth, DB session)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py       # Include all v1 routers
│   │   │   ├── auth.py         # Auth endpoints
│   │   │   ├── tasks.py        # Task CRUD endpoints
│   │   │   └── users.py        # User profile endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # SQLAlchemy User model
│   │   └── task.py             # SQLAlchemy Task model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # Pydantic User schemas
│   │   └── task.py             # Pydantic Task schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Auth business logic
│   │   ├── task_service.py     # Task business logic (from Phase 1)
│   │   └── email_service.py    # Email sending logic
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py  # User DB operations
│   │   └── task_repository.py  # Task DB operations
│   └── utils/
│       ├── __init__.py
│       ├── security.py         # Password hashing, JWT utilities
│       └── email_templates.py  # Email template rendering
├── alembic/
│   ├── versions/               # Migration files
│   └── env.py
├── tests/
│   ├── conftest.py             # Pytest fixtures
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── alembic.ini
├── requirements.txt
└── .env.example
```

**Alternatives Considered**:
- Flat structure: Works for small apps but becomes messy at scale
- DDD (Domain-Driven Design): Too complex for Phase 2 scope
- Feature-based structure: Good for microservices but overkill here

**Implementation Notes**:
- Each router file should be focused on a single resource (tasks, users, auth)
- Services contain business logic (validations, complex operations)
- Repositories handle database queries only (thin data access layer)
- Schemas define request/response models with Pydantic
- Models define database tables with SQLAlchemy

**Gotchas to Avoid**:
- Don't put business logic in route handlers - use services
- Don't access database directly in routes - use repositories
- Don't mix Pydantic schemas with SQLAlchemy models
- Don't create circular imports (dependencies.py helps prevent this)

---

### Async vs Sync Endpoints

**Decision**: Use async endpoints with async database operations

**Rationale**:
- Better performance under concurrent load (multiple users)
- Non-blocking I/O for database queries and external API calls (SendGrid)
- FastAPI is built on ASGI (async-first)
- Neon PostgreSQL supports async drivers (asyncpg)

**Alternatives Considered**:
- Sync endpoints: Simpler but blocks threads, poor performance at scale
- Mixed async/sync: Creates confusion and potential deadlocks

**Implementation Notes**:
- Use `async def` for all route handlers
- Use `asyncpg` driver with SQLAlchemy 2.0 async engine
- Use `httpx.AsyncClient` for external API calls (SendGrid)
- Use `await` for all I/O operations (database, HTTP requests, file operations)

**Async Endpoint Pattern**:
```python
# app/api/v1/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_service = TaskService(db)
    task = await task_service.create_task(task_data, current_user.id)
    return task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

**Database Session Pattern**:
```python
# app/dependencies.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
```

**Gotchas to Avoid**:
- Don't mix sync and async database operations
- Don't forget `await` keyword (will return coroutine object instead of result)
- Don't use sync libraries (requests, psycopg2) - use async alternatives (httpx, asyncpg)
- Don't block the event loop with CPU-intensive tasks (use background tasks)

---

### Dependency Injection Patterns

**Decision**: Use FastAPI's Depends() for dependency injection

**Rationale**:
- Automatic dependency resolution and validation
- Easy to test with dependency overrides
- Clean separation of concerns
- Type-safe with editor support

**Common Dependencies**:
1. **Database Session**: `get_db()`
2. **Current User**: `get_current_user()`
3. **Pagination**: `pagination_params()`
4. **Admin Check**: `require_admin()`

**Implementation Notes**:
```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.utils.security import decode_access_token
from app.repositories.user_repository import UserRepository

security = HTTPBearer()

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def pagination_params(skip: int = 0, limit: int = 50):
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
    return {"skip": skip, "limit": limit}
```

**Usage in Routes**:
```python
@router.get("/tasks")
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    pagination = Depends(pagination_params)
):
    # All dependencies automatically injected
    pass
```

**Testing with Dependency Overrides**:
```python
# tests/conftest.py
from app.main import app
from app.dependencies import get_db, get_current_user

async def override_get_db():
    # Return test database session
    pass

async def override_get_current_user():
    # Return mock user
    return {"id": 1, "email": "test@example.com"}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
```

**Gotchas to Avoid**:
- Don't create dependencies with side effects (should be idempotent)
- Don't nest dependencies too deeply (max 3 levels)
- Don't forget to handle exceptions in dependencies (raise HTTPException)
- Don't use dependencies for request body validation (use Pydantic schemas)

---

### Error Handling and Validation with Pydantic

**Decision**: Use Pydantic v2 for request/response validation + custom exception handlers

**Rationale**:
- Automatic request validation with clear error messages
- Type safety and editor autocomplete
- Consistent error response format across all endpoints
- Aligns with FastAPI's native validation system

**Pydantic Schema Pattern**:
```python
# app/schemas/task.py
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None

class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)
```

**Custom Exception Handlers**:
```python
# app/main.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
            "body": exc.body
        }
    )

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Database Integrity Error",
            "detail": "Resource already exists or constraint violated"
        }
    )

class TaskNotFoundError(Exception):
    pass

@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Task not found", "detail": str(exc)}
    )
```

**Standardized Error Response Format**:
```json
{
  "error": "Error Type",
  "detail": "Human-readable error message",
  "details": [
    {
      "loc": ["body", "field_name"],
      "msg": "Field-specific error message",
      "type": "value_error"
    }
  ]
}
```

**Implementation Notes**:
- Use Pydantic schemas for all request bodies and responses
- Create separate schemas for Create, Update, and Response operations
- Use `Field()` for validation constraints (min_length, max_length, regex)
- Use `@field_validator` for complex validation logic
- Create custom exception classes for domain-specific errors
- Register exception handlers in main.py for consistent responses

**Gotchas to Avoid**:
- Don't validate in route handlers - let Pydantic handle it
- Don't return SQLAlchemy models directly - convert to Pydantic schemas
- Don't forget `from_attributes = True` in Config (for ORM models)
- Don't create too many schema variants - share common base classes

---

## JWT Authentication Implementation

### Access Token + Refresh Token Pattern

**Decision**: Implement dual-token system with short-lived access tokens (24h) and long-lived refresh tokens (7d)

**Rationale**:
- Security: Short access token expiration limits damage from token theft
- UX: Refresh tokens prevent frequent re-authentication
- Revocation: Refresh tokens can be stored in DB and revoked
- Industry standard: OAuth 2.0 pattern widely adopted

**Alternatives Considered**:
- Single long-lived token: Security risk, no way to revoke without DB check on every request
- Session-based auth: Requires server-side session storage, doesn't scale horizontally
- Magic links only: Poor UX for frequent access, no offline support

**Token Structure**:
```python
# Access Token Payload
{
  "sub": "user_id",           # Subject (user ID)
  "email": "user@example.com",
  "exp": 1234567890,          # Expiration (24h from issue)
  "iat": 1234567890,          # Issued at
  "type": "access"
}

# Refresh Token Payload
{
  "sub": "user_id",
  "exp": 1234567890,          # Expiration (7d from issue)
  "iat": 1234567890,
  "jti": "unique_token_id",   # JWT ID (for revocation tracking)
  "type": "refresh"
}
```

**Implementation**:
```python
# app/utils/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets

# Load from environment
SECRET_KEY = "your-secret-key-here"  # Load from config
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access", "iat": datetime.utcnow()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    jti = secrets.token_urlsafe(32)  # Unique token ID for revocation
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "iat": datetime.utcnow(),
        "jti": jti
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

**Login Endpoint**:
```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(
        credentials.email,
        credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Store refresh token in database for revocation capability
    await auth_service.store_refresh_token(user.id, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
```

**Token Refresh Endpoint**:
```python
@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)

    # Validate refresh token
    payload = decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Check if token is revoked
    is_valid = await auth_service.validate_refresh_token(
        user_id=payload["sub"],
        jti=payload["jti"]
    )

    if not is_valid:
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    # Issue new access token
    access_token = create_access_token({
        "sub": payload["sub"],
        "email": payload.get("email")
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,  # Return same refresh token
        "token_type": "bearer"
    }
```

**Implementation Notes**:
- Store refresh tokens in database with user_id, jti, and expiration
- On logout, delete refresh token from database (revocation)
- On password change, delete all user's refresh tokens (force re-login)
- Use `python-jose[cryptography]` for JWT encoding/decoding
- Use `passlib[bcrypt]` for password hashing

**Gotchas to Avoid**:
- Don't use weak SECRET_KEY (use 32+ random bytes, load from environment)
- Don't skip token type validation (prevent refresh token used as access token)
- Don't store access tokens in database (defeats purpose of stateless tokens)
- Don't return sensitive user data in token payload (tokens are readable)

---

### Token Storage Strategy

**Decision**: HttpOnly cookies for web app, with option for Authorization header (for mobile/API clients)

**Rationale**:
- HttpOnly cookies prevent XSS attacks (JavaScript cannot read tokens)
- SameSite=Lax prevents CSRF attacks
- Automatic token sending with requests (no manual header management)
- Fallback to Authorization header for non-browser clients

**Alternatives Considered**:
- localStorage: Vulnerable to XSS attacks, not recommended for sensitive tokens
- sessionStorage: Same XSS vulnerability, data lost on tab close
- Authorization header only: Requires manual token management in frontend

**Implementation**:
```python
# app/api/v1/auth.py
from fastapi import Response

@router.post("/login")
async def login(
    credentials: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    # ... authentication logic ...

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Set httpOnly cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="lax",
        max_age=60 * 60 * 24,  # 24 hours
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return {"message": "Login successful", "user": user_response}
```

**Frontend Token Reading** (for Authorization header fallback):
```typescript
// lib/auth.ts
export async function login(email: string, password: string) {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',  // Send cookies
    body: JSON.stringify({ email, password })
  });

  if (!response.ok) throw new Error('Login failed');

  // Cookies are automatically set, no manual token storage needed
  return response.json();
}

export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  return fetch(url, {
    ...options,
    credentials: 'include',  // Always send cookies
    headers: {
      ...options.headers,
      'Content-Type': 'application/json',
    }
  });
}
```

**Updated Dependency for Cookie/Header Support**:
```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer(auto_error=False)  # Don't auto-error if no header

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    # Try to get token from Authorization header first
    token = None
    if credentials:
        token = credentials.credentials

    # Fallback to cookie
    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
```

**Logout Implementation**:
```python
@router.post("/logout")
async def logout(
    response: Response,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Revoke refresh token in database
    auth_service = AuthService(db)
    await auth_service.revoke_user_tokens(current_user.id)

    # Clear cookies
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message": "Logged out successfully"}
```

**Implementation Notes**:
- Use `secure=True` in production (requires HTTPS)
- Use `samesite="lax"` for balance of security and usability
- Set appropriate `max_age` matching token expiration
- Support both cookies and Authorization header for flexibility
- Clear cookies on logout

**Gotchas to Avoid**:
- Don't set `samesite="strict"` (breaks OAuth redirects and external links)
- Don't forget `credentials: 'include'` in frontend fetch calls
- Don't use cookies for cross-origin requests without proper CORS setup
- Don't set cookies in development without handling localhost properly

---

### Password Reset Flow

**Decision**: Email-based password reset with time-limited tokens (1 hour expiration)

**Rationale**:
- Standard industry practice for account recovery
- Time-limited tokens prevent replay attacks
- Single-use tokens prevent token reuse
- Aligns with SendGrid email integration requirement

**Flow**:
1. User requests password reset (email input)
2. Backend generates reset token (JWT with 1h expiration)
3. Backend sends email with reset link containing token
4. User clicks link, redirected to reset form
5. User submits new password with token
6. Backend validates token and updates password

**Implementation**:
```python
# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

# app/utils/security.py
def create_password_reset_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=1)
    jti = secrets.token_urlsafe(32)
    to_encode = {
        "sub": email,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "password_reset",
        "jti": jti
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_password_reset_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "password_reset":
            return None
        return payload
    except JWTError:
        return None

# app/api/v1/auth.py
@router.post("/password-reset-request")
async def request_password_reset(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(request.email)

    # Always return success (prevent email enumeration)
    if not user:
        return {"message": "If email exists, reset link has been sent"}

    # Generate reset token
    reset_token = create_password_reset_token(user.email)

    # Store token hash in database (for revocation on use)
    await user_repo.store_reset_token(user.id, reset_token)

    # Send email
    email_service = EmailService()
    reset_url = f"https://yourdomain.com/reset-password?token={reset_token}"
    await email_service.send_password_reset_email(user.email, reset_url)

    return {"message": "If email exists, reset link has been sent"}

@router.post("/password-reset-confirm")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    # Validate token
    payload = decode_password_reset_token(reset_data.token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if token has been used
    is_valid = await user_repo.validate_reset_token(user.id, reset_data.token)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Token already used")

    # Update password
    hashed_password = hash_password(reset_data.new_password)
    await user_repo.update_password(user.id, hashed_password)

    # Invalidate reset token and all refresh tokens
    await user_repo.revoke_reset_token(user.id, reset_data.token)
    await user_repo.revoke_all_refresh_tokens(user.id)

    return {"message": "Password reset successful"}
```

**Database Schema for Reset Tokens**:
```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_hash = Column(String, nullable=False, unique=True)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
```

**Frontend Reset Form**:
```typescript
// app/reset-password/page.tsx
'use client';
import { useSearchParams } from 'next/navigation';

export default function ResetPasswordPage() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const newPassword = formData.get('password');

    const response = await fetch('/api/v1/auth/password-reset-confirm', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, new_password: newPassword })
    });

    if (response.ok) {
      // Redirect to login
      window.location.href = '/login';
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="password" name="password" minLength={8} required />
      <button type="submit">Reset Password</button>
    </form>
  );
}
```

**Implementation Notes**:
- Always return success message even if email doesn't exist (prevent enumeration)
- Store token hash in database, not plain token
- Mark token as used after successful reset
- Revoke all refresh tokens on password reset (force re-login)
- Delete expired reset tokens periodically (background job)

**Gotchas to Avoid**:
- Don't reveal whether email exists in system (security risk)
- Don't allow token reuse (mark as used after reset)
- Don't use long expiration times (1 hour max)
- Don't forget to revoke sessions on password change

---

## Neon PostgreSQL Integration

### Connection Pooling Best Practices

**Decision**: Use SQLAlchemy async engine with connection pooling (5-20 connections)

**Rationale**:
- Connection pooling reuses database connections (reduces overhead)
- Async engine supports high concurrency with fewer connections
- Neon serverless architecture benefits from smaller pool sizes
- Aligns with FastAPI async pattern

**Alternatives Considered**:
- Sync engine: Blocks threads, poor performance with async FastAPI
- No pooling: Creates new connection per request (slow, resource-intensive)
- PgBouncer: External pooler, adds complexity for Phase 2 scope

**Implementation**:
```python
# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

# Database URL format: postgresql+asyncpg://user:pass@host/db
DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in development
    pool_size=5,          # Number of persistent connections
    max_overflow=10,      # Additional connections if pool exhausted
    pool_pre_ping=True,   # Verify connections before using (prevents stale connections)
    pool_recycle=3600,    # Recycle connections after 1 hour
)

# Create session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

async def init_db():
    """Create all tables (for development - use Alembic in production)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    """Close all database connections"""
    await engine.dispose()
```

**Configuration**:
```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

**Startup/Shutdown Events**:
```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

app = FastAPI(lifespan=lifespan)
```

**Connection Pool Sizing**:
- **Development**: `pool_size=5, max_overflow=5` (10 total)
- **Production**: `pool_size=10, max_overflow=10` (20 total)
- **Neon Free Tier**: Max 100 connections (keep pool small)

**Implementation Notes**:
- Use `postgresql+asyncpg://` driver (not `postgresql://`)
- Set `pool_pre_ping=True` to handle Neon's serverless auto-pause
- Set `pool_recycle=3600` to prevent stale connections
- Monitor connection pool usage in production (Neon dashboard)
- Adjust pool size based on concurrent request load

**Gotchas to Avoid**:
- Don't set pool_size too high (Neon has connection limits)
- Don't forget to dispose engine on shutdown (connection leaks)
- Don't use sync engine with async FastAPI (blocks event loop)
- Don't skip pool_pre_ping with Neon (handles auto-pause gracefully)

---

### SQLAlchemy Async Pattern

**Decision**: Use SQLAlchemy 2.0 async API throughout

**Rationale**:
- Consistent async/await pattern with FastAPI
- Better performance under load
- Required for asyncpg driver (Neon's recommended driver)
- Future-proof (SQLAlchemy 2.0+ is async-first)

**Model Definition**:
```python
# app/models/task.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship
    user = relationship("User", back_populates="tasks")
```

**Repository Pattern (Async)**:
```python
# app/repositories/task_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.task import Task, TaskStatus
from typing import List, Optional

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task_data: dict) -> Task:
        task = Task(**task_data)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        stmt = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_user(
        self,
        user_id: int,
        status: Optional[TaskStatus] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Task]:
        stmt = select(Task).where(Task.user_id == user_id)

        if status:
            stmt = stmt.where(Task.status == status)

        stmt = stmt.offset(skip).limit(limit).order_by(Task.created_at.desc())

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, task_id: int, user_id: int, updates: dict) -> Optional[Task]:
        stmt = (
            update(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
            .values(**updates)
            .returning(Task)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete(self, task_id: int, user_id: int) -> bool:
        stmt = delete(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0
```

**Usage in Service Layer**:
```python
# app/services/task_service.py
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class TaskService:
    def __init__(self, db: AsyncSession):
        self.repo = TaskRepository(db)

    async def create_task(self, task_data: TaskCreate, user_id: int):
        task_dict = task_data.model_dump()
        task_dict['user_id'] = user_id
        return await self.repo.create(task_dict)

    async def get_task(self, task_id: int, user_id: int):
        return await self.repo.get_by_id(task_id, user_id)

    async def list_tasks(self, user_id: int, **filters):
        return await self.repo.get_all_by_user(user_id, **filters)

    async def update_task(self, task_id: int, user_id: int, updates: TaskUpdate):
        update_dict = updates.model_dump(exclude_unset=True)
        return await self.repo.update(task_id, user_id, update_dict)

    async def delete_task(self, task_id: int, user_id: int):
        return await self.repo.delete(task_id, user_id)
```

**Implementation Notes**:
- Always use `await` with database operations
- Use `select()` construct (not Query API)
- Use `scalar_one_or_none()` for single results
- Use `scalars().all()` for multiple results
- Use `commit()` after write operations
- Use `refresh()` to reload object after commit

**Gotchas to Avoid**:
- Don't forget `await` on database operations
- Don't use lazy loading (not supported in async) - use `selectinload()` for relationships
- Don't access relationships without eager loading
- Don't use `session.query()` (legacy API, use `select()`)

---

### Alembic Migration Workflow

**Decision**: Use Alembic for all database schema changes

**Rationale**:
- Version control for database schema
- Safe, reversible migrations
- Team collaboration (shared migration history)
- Required for production deployments

**Setup**:
```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Configure for async SQLAlchemy
```

**Configuration**:
```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Import your models
from app.database import Base
from app.models.user import User
from app.models.task import Task

config = context.config

# Update sqlalchemy.url from app config
from app.config import settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
```

**Migration Workflow**:
```bash
# Create new migration (auto-generate from model changes)
alembic revision --autogenerate -m "create tasks table"

# Review generated migration in alembic/versions/

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Check current version
alembic current

# View migration history
alembic history
```

**Example Migration**:
```python
# alembic/versions/001_create_tasks_table.py
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('status', sa.Enum('pending', 'completed', name='taskstatus'), nullable=False),
        sa.Column('priority', sa.Enum('low', 'medium', 'high', name='taskpriority'), nullable=False),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    op.create_index(op.f('ix_tasks_user_id'), 'tasks', ['user_id'], unique=False)
    op.create_index(op.f('ix_tasks_created_at'), 'tasks', ['created_at'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_tasks_created_at'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_user_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
```

**Implementation Notes**:
- Always review auto-generated migrations before applying
- Add indexes in migrations, not just in models
- Use descriptive migration messages
- Never edit applied migrations (create new one to fix)
- Commit migrations to git with code changes

**Gotchas to Avoid**:
- Don't skip migration review (auto-generate can miss things)
- Don't modify applied migrations (breaks team sync)
- Don't apply migrations directly in production without testing
- Don't forget to import all models in env.py (or autogenerate won't detect them)

---

### Index Strategy

**Decision**: Index `user_id`, `created_at`, and composite `(user_id, status)` for common queries

**Rationale**:
- Most queries filter by user_id (multi-tenant isolation)
- Listing tasks sorted by created_at is common
- Filtering by status within user tasks is frequent
- Composite index optimizes filtered queries

**Index Definitions**:
```python
# app/models/task.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Index
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Composite index for common query patterns
    __table_args__ = (
        Index('ix_tasks_user_status', 'user_id', 'status'),
        Index('ix_tasks_user_created', 'user_id', 'created_at'),
    )
```

**Query Optimization**:
```python
# Optimized by ix_tasks_user_status
stmt = select(Task).where(
    Task.user_id == user_id,
    Task.status == TaskStatus.PENDING
)

# Optimized by ix_tasks_user_created
stmt = select(Task).where(
    Task.user_id == user_id
).order_by(Task.created_at.desc())
```

**Implementation Notes**:
- Primary key (id) is automatically indexed
- Foreign keys (user_id) should be indexed
- Columns used in WHERE, ORDER BY, and JOIN should be indexed
- Composite indexes should match query patterns (order matters)
- Don't over-index (slows writes)

**Gotchas to Avoid**:
- Don't index low-cardinality columns (e.g., boolean flags)
- Don't create redundant indexes (user_id, status) + (user_id) - first covers second
- Don't forget to add indexes in Alembic migrations
- Don't index every column (balance read vs write performance)

---

## SendGrid Email Integration

### Email Service Best Practices

**Decision**: Use SendGrid Python SDK with async HTTP client (httpx)

**Rationale**:
- SendGrid has generous free tier (100 emails/day)
- Official Python SDK simplifies API integration
- Async client prevents blocking FastAPI event loop
- Supports templates and analytics

**Alternatives Considered**:
- SMTP: More complex setup, no analytics, rate limiting issues
- Mailgun: Similar to SendGrid, no clear advantage
- AWS SES: More complex setup, requires AWS account

**Setup**:
```bash
pip install sendgrid httpx
```

**Implementation**:
```python
# app/services/email_service.py
import httpx
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.config import settings
from typing import List

class EmailService:
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.FROM_EMAIL
        self.client = SendGridAPIClient(self.api_key)

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_content: str = None
    ) -> bool:
        """Send email via SendGrid API"""
        message = Mail(
            from_email=Email(self.from_email),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )

        if plain_content:
            message.add_content(Content("text/plain", plain_content))

        try:
            # Use httpx for async HTTP request
            async with httpx.AsyncClient() as http_client:
                response = await http_client.post(
                    "https://api.sendgrid.com/v3/mail/send",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=message.get()
                )
                response.raise_for_status()
                return True
        except httpx.HTTPError as e:
            # Log error (use logging module)
            print(f"Email send failed: {e}")
            return False

    async def send_welcome_email(self, to_email: str, username: str):
        """Send welcome email to new user"""
        html_content = f"""
        <h1>Welcome to Todo App, {username}!</h1>
        <p>Thanks for signing up. Get started by creating your first task.</p>
        <a href="https://yourdomain.com/tasks">Go to Dashboard</a>
        """
        plain_content = f"Welcome to Todo App, {username}! Visit https://yourdomain.com/tasks to get started."

        return await self.send_email(
            to_email=to_email,
            subject="Welcome to Todo App",
            html_content=html_content,
            plain_content=plain_content
        )

    async def send_password_reset_email(self, to_email: str, reset_url: str):
        """Send password reset email"""
        html_content = f"""
        <h1>Password Reset Request</h1>
        <p>Click the link below to reset your password:</p>
        <a href="{reset_url}">Reset Password</a>
        <p>This link expires in 1 hour.</p>
        <p>If you didn't request this, please ignore this email.</p>
        """
        plain_content = f"Reset your password: {reset_url}\n\nThis link expires in 1 hour."

        return await self.send_email(
            to_email=to_email,
            subject="Password Reset Request",
            html_content=html_content,
            plain_content=plain_content
        )
```

**Configuration**:
```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SENDGRID_API_KEY: str
    FROM_EMAIL: str = "noreply@yourdomain.com"

    class Config:
        env_file = ".env"
```

**Usage in Routes**:
```python
# app/api/v1/auth.py
@router.post("/register")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # ... create user logic ...

    # Send welcome email (non-blocking)
    email_service = EmailService()
    await email_service.send_welcome_email(user.email, user.email.split('@')[0])

    return {"message": "Registration successful"}
```

**Implementation Notes**:
- Use environment variables for API key and from email
- Always provide both HTML and plain text versions
- Use async HTTP client (httpx) to avoid blocking
- Handle email failures gracefully (don't fail registration if email fails)
- Log email send failures for monitoring

**Gotchas to Avoid**:
- Don't use sync SendGrid client (blocks event loop)
- Don't hard-code API keys (use environment variables)
- Don't fail user operations if email fails (email is secondary)
- Don't send emails synchronously (use background tasks for non-critical emails)

---

### Email Template Best Practices

**Decision**: Use Python template strings for simple emails, migrate to SendGrid templates for complex designs

**Rationale**:
- Template strings sufficient for Phase 2 (welcome, password reset)
- SendGrid templates add complexity (HTML editor, versioning)
- Easy to migrate later if design needs increase

**Template Organization**:
```python
# app/utils/email_templates.py
from typing import Dict

def render_template(template_name: str, context: Dict[str, str]) -> tuple[str, str]:
    """Render email template with context"""
    templates = {
        "welcome": {
            "html": """
                <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h1 style="color: #333;">Welcome to Todo App, {username}!</h1>
                    <p>Thanks for signing up. Get started by creating your first task.</p>
                    <a href="{dashboard_url}"
                       style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">
                        Go to Dashboard
                    </a>
                    <p style="color: #666; margin-top: 20px;">
                        If you have any questions, reply to this email.
                    </p>
                </body>
                </html>
            """,
            "plain": "Welcome to Todo App, {username}!\n\nVisit {dashboard_url} to get started."
        },
        "password_reset": {
            "html": """
                <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h1 style="color: #333;">Password Reset Request</h1>
                    <p>Click the button below to reset your password:</p>
                    <a href="{reset_url}"
                       style="display: inline-block; padding: 10px 20px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 5px;">
                        Reset Password
                    </a>
                    <p style="color: #666; margin-top: 20px;">
                        This link expires in 1 hour.
                    </p>
                    <p style="color: #666;">
                        If you didn't request this, please ignore this email.
                    </p>
                </body>
                </html>
            """,
            "plain": "Reset your password: {reset_url}\n\nThis link expires in 1 hour.\n\nIf you didn't request this, ignore this email."
        }
    }

    template = templates.get(template_name)
    if not template:
        raise ValueError(f"Template {template_name} not found")

    html_content = template["html"].format(**context)
    plain_content = template["plain"].format(**context)

    return html_content, plain_content

# Usage
html, plain = render_template("welcome", {
    "username": "John",
    "dashboard_url": "https://yourdomain.com/tasks"
})
```

**Implementation Notes**:
- Keep templates simple and readable
- Always provide plain text alternative
- Use inline CSS for email (better client support)
- Test emails in multiple clients (Gmail, Outlook, Apple Mail)
- Include unsubscribe link for marketing emails (not required for transactional)

**Gotchas to Avoid**:
- Don't use external CSS (not supported in many email clients)
- Don't use JavaScript (blocked by all email clients)
- Don't forget to escape user input in templates (XSS risk)
- Don't use complex HTML/CSS (breaks in many clients)

---

### Rate Limiting and Error Handling

**Decision**: Implement application-level rate limiting + graceful degradation on email failures

**Rationale**:
- Prevent abuse (spam, password reset attacks)
- Stay within SendGrid limits (100/day free tier)
- User operations should succeed even if email fails
- Retry logic for transient failures

**Rate Limiting**:
```python
# app/utils/rate_limiter.py
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict

class EmailRateLimiter:
    def __init__(self, max_per_hour: int = 10, max_per_day: int = 50):
        self.max_per_hour = max_per_hour
        self.max_per_day = max_per_day
        self.email_log: Dict[str, list] = defaultdict(list)

    def can_send(self, email: str) -> bool:
        """Check if email can be sent based on rate limits"""
        now = datetime.utcnow()
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)

        # Clean old entries
        self.email_log[email] = [
            ts for ts in self.email_log[email] if ts > day_ago
        ]

        recent = self.email_log[email]
        hour_count = sum(1 for ts in recent if ts > hour_ago)
        day_count = len(recent)

        if hour_count >= self.max_per_hour or day_count >= self.max_per_day:
            return False

        self.email_log[email].append(now)
        return True

# Global rate limiter
email_rate_limiter = EmailRateLimiter(max_per_hour=10, max_per_day=50)
```

**Error Handling with Retry**:
```python
# app/services/email_service.py
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

class EmailService:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def send_email_with_retry(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_content: str = None
    ) -> bool:
        """Send email with automatic retry on transient failures"""

        # Check rate limit
        if not email_rate_limiter.can_send(to_email):
            raise ValueError(f"Rate limit exceeded for {to_email}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as http_client:
                response = await http_client.post(
                    "https://api.sendgrid.com/v3/mail/send",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=self._build_message(to_email, subject, html_content, plain_content)
                )

                if response.status_code == 429:  # Rate limited by SendGrid
                    raise Exception("SendGrid rate limit exceeded")

                response.raise_for_status()
                return True

        except httpx.TimeoutException:
            # Retry on timeout
            raise
        except httpx.HTTPStatusError as e:
            if e.response.status_code >= 500:
                # Retry on server errors
                raise
            else:
                # Don't retry on client errors (4xx)
                print(f"Email send failed (client error): {e}")
                return False
        except Exception as e:
            print(f"Email send failed: {e}")
            return False
```

**Graceful Degradation in Routes**:
```python
# app/api/v1/auth.py
@router.post("/register")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Create user first
    user = await auth_service.create_user(user_data)

    # Try to send welcome email (non-blocking, failure doesn't affect registration)
    try:
        email_service = EmailService()
        await email_service.send_email_with_retry(
            user.email,
            "Welcome to Todo App",
            html_content,
            plain_content
        )
    except Exception as e:
        # Log error but don't fail registration
        print(f"Failed to send welcome email: {e}")

    return {"message": "Registration successful", "user": user}
```

**Implementation Notes**:
- Track email sends per user for rate limiting
- Retry on transient errors (5xx, timeouts)
- Don't retry on client errors (4xx, invalid email)
- Log all email failures for monitoring
- Never fail user operations due to email failures

**Gotchas to Avoid**:
- Don't block user operations waiting for email
- Don't retry indefinitely (max 3 attempts)
- Don't fail silently (log all failures)
- Don't send sensitive data in email logs (GDPR)

---

### Testing Email Flows

**Decision**: Use email capture in development + mock service in tests

**Rationale**:
- Avoid sending real emails during development
- Fast test execution without external API calls
- Verify email content without checking inbox
- Easy to reset between tests

**Development Email Capture**:
```python
# app/config.py
class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    SENDGRID_API_KEY: str
    EMAIL_CAPTURE_MODE: bool = True  # Capture emails instead of sending

# app/services/email_service.py
class EmailService:
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.FROM_EMAIL
        self.capture_mode = settings.EMAIL_CAPTURE_MODE
        self.captured_emails = []  # Store in memory for dev

    async def send_email(self, to_email: str, subject: str, html_content: str, plain_content: str = None):
        if self.capture_mode:
            # Capture email instead of sending
            self.captured_emails.append({
                "to": to_email,
                "subject": subject,
                "html": html_content,
                "plain": plain_content,
                "sent_at": datetime.utcnow()
            })
            print(f"[EMAIL CAPTURED] To: {to_email}, Subject: {subject}")
            return True

        # Send real email in production
        return await self._send_via_sendgrid(to_email, subject, html_content, plain_content)
```

**Test Mock**:
```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_email_service():
    """Mock email service for testing"""
    service = AsyncMock()
    service.send_email.return_value = True
    service.send_welcome_email.return_value = True
    service.send_password_reset_email.return_value = True
    return service

# tests/integration/test_auth.py
async def test_registration_sends_welcome_email(client, mock_email_service, monkeypatch):
    # Replace real email service with mock
    monkeypatch.setattr("app.services.email_service.EmailService", lambda: mock_email_service)

    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "securepass123"
    })

    assert response.status_code == 201

    # Verify email was sent
    mock_email_service.send_welcome_email.assert_called_once_with(
        "test@example.com",
        "test"
    )

async def test_registration_succeeds_even_if_email_fails(client, mock_email_service, monkeypatch):
    # Simulate email failure
    mock_email_service.send_welcome_email.side_effect = Exception("SendGrid error")
    monkeypatch.setattr("app.services.email_service.EmailService", lambda: mock_email_service)

    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "securepass123"
    })

    # Registration should still succeed
    assert response.status_code == 201
```

**Development Email Viewer** (optional):
```python
# app/api/v1/dev.py (only in development)
from fastapi import APIRouter
from app.services.email_service import EmailService

router = APIRouter(prefix="/dev", tags=["development"])

@router.get("/emails")
async def list_captured_emails():
    """View captured emails in development"""
    if not settings.EMAIL_CAPTURE_MODE:
        raise HTTPException(status_code=404, detail="Only available in dev mode")

    email_service = EmailService()
    return {"emails": email_service.captured_emails}

@router.delete("/emails")
async def clear_captured_emails():
    """Clear captured emails"""
    if not settings.EMAIL_CAPTURE_MODE:
        raise HTTPException(status_code=404, detail="Only available in dev mode")

    email_service = EmailService()
    email_service.captured_emails.clear()
    return {"message": "Cleared captured emails"}
```

**Implementation Notes**:
- Use capture mode in development and testing
- Use real SendGrid in production
- Mock email service in unit/integration tests
- Verify email content and recipients in tests
- Test graceful degradation when email fails

**Gotchas to Avoid**:
- Don't send real emails in tests (slow, consumes quota)
- Don't skip email tests (critical for user flows)
- Don't forget to clear mocks between tests
- Don't expose captured emails in production (privacy risk)

---

## Frontend-Backend Communication

### CORS Configuration

**Decision**: Configure CORS to allow Next.js frontend (http://localhost:3000 in dev, production domain in prod)

**Rationale**:
- Next.js frontend runs on different port/domain than FastAPI backend
- Browser enforces CORS for security
- Need to allow credentials (cookies) for authentication
- Restrict to specific origins for security

**Implementation**:
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI()

# CORS configuration
origins = []

if settings.ENVIRONMENT == "development":
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
else:
    origins = [
        "https://yourdomain.com",
        "https://www.yourdomain.com",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Length", "X-Total-Count"],
    max_age=600,  # Cache preflight requests for 10 minutes
)
```

**Configuration**:
```python
# app/config.py
class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

# .env
ENVIRONMENT=development
FRONTEND_URL=http://localhost:3000
```

**Frontend Fetch Configuration**:
```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    credentials: 'include',  // Send cookies
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
}
```

**Implementation Notes**:
- Use environment-specific origins
- Enable credentials for cookie-based auth
- Restrict methods to only what's needed
- Set reasonable max_age for preflight caching
- Never use `allow_origins=["*"]` with `allow_credentials=True`

**Gotchas to Avoid**:
- Don't allow all origins in production (`*` is insecure)
- Don't forget `credentials: 'include'` in frontend
- Don't allow credentials with wildcard origins (browser blocks it)
- Don't forget to add production domain to origins list

---

### API Versioning Strategy

**Decision**: Use URL path versioning (`/api/v1/...`)

**Rationale**:
- Clear version in URL (easy to understand)
- Simple to implement with FastAPI routers
- Easy to maintain multiple versions simultaneously
- Industry standard (RESTful API best practice)

**Alternatives Considered**:
- Header versioning: Less visible, harder to test in browser
- Query parameter: Not RESTful, easy to forget
- Content negotiation: Complex, overkill for Phase 2

**Implementation**:
```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1 import auth, tasks, users

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(tasks.router)
router.include_router(users.router)

# app/main.py
from app.api.v1.router import router as v1_router

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.include_router(v1_router)
```

**URL Structure**:
```
/api/v1/auth/login
/api/v1/auth/register
/api/v1/auth/logout
/api/v1/tasks
/api/v1/tasks/{task_id}
/api/v1/users/me
```

**Frontend API Client**:
```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_VERSION = 'v1';

export const endpoints = {
  auth: {
    login: `/api/${API_VERSION}/auth/login`,
    register: `/api/${API_VERSION}/auth/register`,
    logout: `/api/${API_VERSION}/auth/logout`,
    refresh: `/api/${API_VERSION}/auth/refresh`,
  },
  tasks: {
    list: `/api/${API_VERSION}/tasks`,
    create: `/api/${API_VERSION}/tasks`,
    get: (id: number) => `/api/${API_VERSION}/tasks/${id}`,
    update: (id: number) => `/api/${API_VERSION}/tasks/${id}`,
    delete: (id: number) => `/api/${API_VERSION}/tasks/${id}`,
  },
  users: {
    me: `/api/${API_VERSION}/users/me`,
  },
};
```

**Implementation Notes**:
- Start with v1 from the beginning
- Include version in all endpoints
- Document breaking changes in API changelog
- Consider deprecation policy for future versions
- Keep v1 stable throughout Phase 2

**Gotchas to Avoid**:
- Don't change v1 endpoints in breaking ways (create v2 instead)
- Don't mix versioning strategies (pick one and stick with it)
- Don't skip version in critical endpoints (inconsistent API)
- Don't version too aggressively (v1 should last multiple phases)

---

### Request/Response Error Standardization

**Decision**: Use consistent error response format across all endpoints

**Rationale**:
- Frontend can handle errors predictably
- Better developer experience
- Easier to debug issues
- Aligns with industry standards (RFC 7807 Problem Details)

**Error Response Format**:
```json
{
  "error": "ErrorType",
  "detail": "Human-readable error message",
  "status_code": 400,
  "timestamp": "2025-12-07T10:30:00Z",
  "path": "/api/v1/tasks",
  "request_id": "abc123-def456"
}
```

**Implementation**:
```python
# app/schemas/error.py
from pydantic import BaseModel
from datetime import datetime

class ErrorResponse(BaseModel):
    error: str
    detail: str
    status_code: int
    timestamp: datetime
    path: str
    request_id: str | None = None

# app/main.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "detail": "An unexpected error occurred",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
            "request_id": getattr(request.state, "request_id", None)
        }
    )

# Custom exception classes
class TaskNotFoundError(Exception):
    pass

@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "TaskNotFound",
            "detail": str(exc) or "Task not found",
            "status_code": 404,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
            "request_id": getattr(request.state, "request_id", None)
        }
    )
```

**Frontend Error Handling**:
```typescript
// lib/api.ts
export class APIError extends Error {
  constructor(
    public error: string,
    public detail: string,
    public statusCode: number,
    public timestamp: string,
    public path: string,
    public requestId?: string
  ) {
    super(detail);
    this.name = 'APIError';
  }
}

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new APIError(
      errorData.error,
      errorData.detail,
      errorData.status_code,
      errorData.timestamp,
      errorData.path,
      errorData.request_id
    );
  }

  return response.json();
}

// Usage in component
async function handleSubmit() {
  try {
    await apiRequest('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData)
    });
  } catch (error) {
    if (error instanceof APIError) {
      if (error.statusCode === 401) {
        // Redirect to login
        router.push('/login');
      } else {
        // Show error message
        setError(error.detail);
      }
    }
  }
}
```

**Common Error Types**:
- `ValidationError` (422): Invalid request data
- `Unauthorized` (401): Not authenticated
- `Forbidden` (403): Authenticated but not authorized
- `NotFound` (404): Resource doesn't exist
- `Conflict` (409): Resource already exists
- `InternalServerError` (500): Unexpected error

**Implementation Notes**:
- Include request_id for debugging
- Include timestamp for log correlation
- Include path for context
- Use descriptive error types
- Provide actionable error messages

**Gotchas to Avoid**:
- Don't expose sensitive information in error messages (stack traces, DB details)
- Don't use generic error messages (be specific)
- Don't return different formats for different errors (consistency)
- Don't forget to log errors server-side (error messages alone aren't enough)

---

### Authentication Header Format

**Decision**: Support both Bearer tokens (Authorization header) and httpOnly cookies

**Rationale**:
- Cookies for web app (automatic, secure)
- Bearer tokens for API clients (mobile apps, Postman)
- Flexibility for different client types
- Industry standard (OAuth 2.0)

**Authorization Header Format**:
```
Authorization: Bearer <access_token>
```

**Implementation** (already covered in JWT section):
```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    # Try Authorization header first
    token = None
    if credentials:
        token = credentials.credentials

    # Fallback to cookie
    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Validate token...
```

**Frontend Usage**:
```typescript
// For cookie-based auth (default)
await fetch('/api/v1/tasks', {
  credentials: 'include'  // Sends cookies automatically
});

// For token-based auth (alternative)
await fetch('/api/v1/tasks', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

**Implementation Notes**:
- Prefer cookies for web app (more secure)
- Support Bearer tokens for non-browser clients
- Always validate token format before decoding
- Return 401 if token is missing or invalid
- Include WWW-Authenticate header in 401 responses

**Gotchas to Avoid**:
- Don't accept tokens from query parameters (security risk)
- Don't validate both cookie and header (choose one per request)
- Don't forget to strip "Bearer " prefix from header
- Don't expose tokens in logs or error messages

---

## Testing Strategies

### Backend Testing with pytest

**Decision**: Use pytest with async support, fixtures for test database, and comprehensive test coverage

**Rationale**:
- pytest is Python testing standard
- Async support via pytest-asyncio
- Fixtures enable clean test database setup/teardown
- Easy to run subset of tests (unit, integration, e2e)

**Setup**:
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

**Configuration**:
```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
markers =
    unit: Unit tests (fast, no external dependencies)
    integration: Integration tests (database, external services)
    e2e: End-to-end tests (full request/response cycle)
```

**Test Database Setup**:
```python
# tests/conftest.py
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.database import Base
from app.main import app
from app.dependencies import get_db
from httpx import AsyncClient

# Test database URL (SQLite for fast tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_engine():
    """Create test database engine"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session(db_engine):
    """Create test database session"""
    async_session_maker = async_sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session

@pytest.fixture(scope="function")
async def client(db_session):
    """Create test client with test database"""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(db_session):
    """Create test user"""
    from app.models.user import User
    from app.utils.security import hash_password

    user = User(
        email="test@example.com",
        hashed_password=hash_password("testpass123")
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def auth_headers(test_user):
    """Get auth headers for test user"""
    from app.utils.security import create_access_token

    token = create_access_token({"sub": str(test_user.id), "email": test_user.email})
    return {"Authorization": f"Bearer {token}"}
```

**Unit Test Example**:
```python
# tests/unit/test_security.py
import pytest
from app.utils.security import hash_password, verify_password, create_access_token, decode_access_token

@pytest.mark.unit
def test_password_hashing():
    password = "securepassword123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

@pytest.mark.unit
def test_access_token_creation_and_decoding():
    payload = {"sub": "123", "email": "test@example.com"}
    token = create_access_token(payload)

    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "123"
    assert decoded["email"] == "test@example.com"
    assert decoded["type"] == "access"
```

**Integration Test Example**:
```python
# tests/integration/test_task_service.py
import pytest
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate

@pytest.mark.integration
async def test_create_task(db_session, test_user):
    service = TaskService(db_session)

    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        priority="high"
    )

    task = await service.create_task(task_data, test_user.id)

    assert task.id is not None
    assert task.title == "Test Task"
    assert task.user_id == test_user.id
    assert task.status == "pending"

@pytest.mark.integration
async def test_list_user_tasks(db_session, test_user):
    service = TaskService(db_session)

    # Create multiple tasks
    for i in range(3):
        await service.create_task(
            TaskCreate(title=f"Task {i}"),
            test_user.id
        )

    tasks = await service.list_tasks(test_user.id)
    assert len(tasks) == 3
```

**E2E Test Example**:
```python
# tests/e2e/test_auth_flow.py
import pytest

@pytest.mark.e2e
async def test_full_registration_and_login_flow(client):
    # Register
    register_response = await client.post("/api/v1/auth/register", json={
        "email": "newuser@example.com",
        "password": "securepass123"
    })
    assert register_response.status_code == 201

    # Login
    login_response = await client.post("/api/v1/auth/login", json={
        "email": "newuser@example.com",
        "password": "securepass123"
    })
    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data

    # Access protected endpoint
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    me_response = await client.get("/api/v1/users/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "newuser@example.com"

@pytest.mark.e2e
async def test_task_crud_flow(client, auth_headers):
    # Create task
    create_response = await client.post(
        "/api/v1/tasks",
        headers=auth_headers,
        json={"title": "Test Task", "priority": "high"}
    )
    assert create_response.status_code == 201
    task = create_response.json()
    task_id = task["id"]

    # List tasks
    list_response = await client.get("/api/v1/tasks", headers=auth_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1

    # Update task
    update_response = await client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers,
        json={"status": "completed"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "completed"

    # Delete task
    delete_response = await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert delete_response.status_code == 204
```

**Running Tests**:
```bash
# All tests
pytest

# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# E2E tests
pytest -m e2e

# With coverage
pytest --cov=app --cov-report=html

# Specific file
pytest tests/e2e/test_auth_flow.py -v
```

**Implementation Notes**:
- Use in-memory SQLite for fast test database
- Create fresh database for each test (function scope)
- Use fixtures for common setup (test user, auth headers)
- Mock external services (SendGrid) in tests
- Aim for 80%+ code coverage

**Gotchas to Avoid**:
- Don't use production database for tests
- Don't share state between tests (use function-scoped fixtures)
- Don't skip test cleanup (database, mocks)
- Don't test implementation details (test behavior)

---

### Frontend Testing with Jest/Vitest

**Decision**: Use Vitest for unit/component tests, Playwright for E2E

**Rationale**:
- Vitest is faster than Jest and has better ESM support
- Native TypeScript support
- Compatible with Vite (common in modern Next.js projects)
- Playwright for full browser E2E tests

**Alternatives Considered**:
- Jest: Slower, requires more configuration for ESM/TypeScript
- React Testing Library + Jest: Good but Vitest is faster
- Cypress: Good for E2E but Playwright has better API and performance

**Setup**:
```bash
# Install Vitest and testing libraries
npm install -D vitest @testing-library/react @testing-library/jest-dom @vitejs/plugin-react

# Install Playwright
npm install -D @playwright/test
npx playwright install
```

**Configuration**:
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './'),
    },
  },
});

// tests/setup.ts
import '@testing-library/jest-dom';
```

**Unit Test Example**:
```typescript
// lib/validators.test.ts
import { describe, it, expect } from 'vitest';
import { validateEmail, validatePassword } from './validators';

describe('validateEmail', () => {
  it('should validate correct email', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });

  it('should reject invalid email', () => {
    expect(validateEmail('invalid-email')).toBe(false);
  });
});

describe('validatePassword', () => {
  it('should validate password with 8+ characters', () => {
    expect(validatePassword('securepass123')).toBe(true);
  });

  it('should reject short password', () => {
    expect(validatePassword('short')).toBe(false);
  });
});
```

**Component Test Example**:
```typescript
// components/TaskCard.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskCard } from './TaskCard';

describe('TaskCard', () => {
  const mockTask = {
    id: 1,
    title: 'Test Task',
    description: 'Test Description',
    status: 'pending',
    priority: 'high',
    created_at: '2025-12-07T10:00:00Z',
  };

  it('should render task information', () => {
    render(<TaskCard task={mockTask} />);

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByText('high')).toBeInTheDocument();
  });

  it('should call onComplete when complete button clicked', () => {
    const onComplete = vi.fn();
    render(<TaskCard task={mockTask} onComplete={onComplete} />);

    const completeButton = screen.getByRole('button', { name: /complete/i });
    fireEvent.click(completeButton);

    expect(onComplete).toHaveBeenCalledWith(1);
  });
});
```

**API Mock Example**:
```typescript
// lib/api.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { apiRequest } from './api';

global.fetch = vi.fn();

describe('apiRequest', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should make successful request', async () => {
    const mockResponse = { data: 'test' };
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const result = await apiRequest('/api/v1/tasks');

    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/tasks',
      expect.objectContaining({
        credentials: 'include',
      })
    );
    expect(result).toEqual(mockResponse);
  });

  it('should throw error on failed request', async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: 'Not found' }),
    });

    await expect(apiRequest('/api/v1/tasks/999')).rejects.toThrow('Not found');
  });
});
```

**Running Tests**:
```bash
# Run all unit/component tests
npm run test

# Run in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage
```

**Implementation Notes**:
- Use `@testing-library/react` for component tests
- Mock API calls in component tests
- Test user interactions with `fireEvent` or `userEvent`
- Use `vi.fn()` for mocking functions
- Aim for 70%+ coverage on components

**Gotchas to Avoid**:
- Don't test implementation details (test behavior)
- Don't mock too much (test real component logic when possible)
- Don't forget to cleanup after tests
- Don't skip accessibility tests (use `getByRole`, `getByLabelText`)

---

### E2E Testing with Playwright

**Decision**: Use Playwright for critical user flows (auth, task CRUD)

**Rationale**:
- Tests full stack (frontend + backend)
- Cross-browser testing (Chromium, Firefox, WebKit)
- Better API than Selenium/Cypress
- Auto-wait for elements (less flaky tests)

**Configuration**:
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

**E2E Test Example**:
```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should register new user and login', async ({ page }) => {
    // Visit registration page
    await page.goto('/register');

    // Fill registration form
    await page.fill('input[name="email"]', 'newuser@example.com');
    await page.fill('input[name="password"]', 'securepass123');
    await page.click('button[type="submit"]');

    // Should redirect to login
    await expect(page).toHaveURL('/login');

    // Login with new credentials
    await page.fill('input[name="email"]', 'newuser@example.com');
    await page.fill('input[name="password"]', 'securepass123');
    await page.click('button[type="submit"]');

    // Should redirect to dashboard
    await expect(page).toHaveURL('/tasks');
    await expect(page.locator('h1')).toContainText('My Tasks');
  });

  test('should show error on invalid login', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[name="email"]', 'invalid@example.com');
    await page.fill('input[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    // Should show error message
    await expect(page.locator('[role="alert"]')).toContainText('Incorrect email or password');
  });
});

// tests/e2e/tasks.spec.ts
test.describe('Task Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'testpass123');
    await page.click('button[type="submit"]');
    await page.waitForURL('/tasks');
  });

  test('should create new task', async ({ page }) => {
    // Click add task button
    await page.click('button:has-text("Add Task")');

    // Fill task form
    await page.fill('input[name="title"]', 'New E2E Task');
    await page.fill('textarea[name="description"]', 'Created by E2E test');
    await page.selectOption('select[name="priority"]', 'high');
    await page.click('button[type="submit"]');

    // Should see new task in list
    await expect(page.locator('text=New E2E Task')).toBeVisible();
    await expect(page.locator('text=Created by E2E test')).toBeVisible();
  });

  test('should mark task as complete', async ({ page }) => {
    // Find first task and click complete button
    const firstTask = page.locator('[data-testid="task-card"]').first();
    await firstTask.locator('button:has-text("Complete")').click();

    // Should show as completed
    await expect(firstTask).toHaveClass(/completed/);
  });

  test('should filter tasks by status', async ({ page }) => {
    // Click pending filter
    await page.click('button:has-text("Pending")');

    // Should only show pending tasks
    const tasks = page.locator('[data-testid="task-card"]');
    await expect(tasks).not.toHaveClass(/completed/);

    // Click completed filter
    await page.click('button:has-text("Completed")');

    // Should only show completed tasks
    await expect(tasks).toHaveClass(/completed/);
  });
});
```

**Running E2E Tests**:
```bash
# Run all E2E tests
npx playwright test

# Run in UI mode (interactive)
npx playwright test --ui

# Run specific test file
npx playwright test auth.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed

# Generate test report
npx playwright show-report
```

**Implementation Notes**:
- Test critical user flows only (don't test every interaction)
- Use `data-testid` attributes for reliable selectors
- Use auto-wait (don't add manual sleeps)
- Run against local development environment
- Clean test data after tests (or use separate test database)

**Gotchas to Avoid**:
- Don't use CSS selectors that change often (use test IDs)
- Don't add manual waits (Playwright auto-waits)
- Don't test everything with E2E (slow, use unit/component tests for details)
- Don't skip cleanup (test data pollution)

---

## Deployment Considerations

### Vercel Deployment for Next.js

**Decision**: Deploy Next.js frontend to Vercel (official Next.js hosting platform)

**Rationale**:
- Zero-config deployment for Next.js
- Automatic HTTPS and CDN
- Preview deployments for PRs
- Serverless functions for API routes (if needed)
- Free tier sufficient for Phase 2

**Setup**:
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel
```

**Configuration**:
```json
// vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "https://api.yourdomain.com"
  }
}
```

**Environment Variables** (set in Vercel dashboard):
```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

**Custom Domain**:
1. Add domain in Vercel dashboard
2. Update DNS records (CNAME to `cname.vercel-dns.com`)
3. Automatic HTTPS certificate provisioning

**Implementation Notes**:
- Use `NEXT_PUBLIC_` prefix for client-side env vars
- Set environment variables in Vercel dashboard (not .env in repo)
- Use preview deployments for testing before production
- Configure CORS in backend to allow Vercel domain

**Gotchas to Avoid**:
- Don't commit `.env` files to git (security risk)
- Don't forget to set environment variables in Vercel
- Don't skip preview deployment testing (catch issues early)
- Don't use server-side env vars in client components (undefined)

---

### FastAPI Backend Deployment (Railway vs Render)

**Decision**: Use Railway for FastAPI backend (better DX than Render)

**Rationale**:
- Simple deployment from GitHub
- Automatic HTTPS
- Built-in PostgreSQL (can use Neon instead)
- Better free tier than Render (500 hours/month)
- Simpler configuration than Render

**Alternatives Considered**:
- Render: Similar features but more complex configuration
- DigitalOcean App Platform: More expensive
- AWS/GCP: Too complex for Phase 2

**Railway Setup**:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

**Configuration**:
```toml
# railway.toml
[build]
builder = "NIXPACKS"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

**Environment Variables** (set in Railway dashboard):
```
DATABASE_URL=postgresql://...  # Neon PostgreSQL URL
SECRET_KEY=your-secret-key-here
SENDGRID_API_KEY=your-sendgrid-key
ENVIRONMENT=production
FRONTEND_URL=https://yourdomain.com
```

**Dockerfile** (optional, for custom build):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
```

**Implementation Notes**:
- Connect GitHub repo for automatic deployments
- Set environment variables in Railway dashboard
- Use Neon PostgreSQL (don't use Railway's built-in Postgres)
- Configure health check endpoint (`/health`)
- Monitor logs in Railway dashboard

**Gotchas to Avoid**:
- Don't commit secrets to git (use Railway env vars)
- Don't forget to set `$PORT` variable (Railway assigns dynamic port)
- Don't use Railway's free Postgres (use Neon for consistency)
- Don't skip health check endpoint (for monitoring)

---

### Environment Variable Management

**Decision**: Use platform-specific environment variable management (Vercel, Railway dashboards) + `.env.example` in repo

**Rationale**:
- Secrets never committed to git
- Platform-specific variables stay in platform
- `.env.example` documents required variables
- Different values for dev/staging/production

**Repository Structure**:
```
.env.example          # Template (committed to git)
.env.local            # Local development (ignored by git)
.gitignore            # Must include .env*
```

**Example `.env.example`**:
```bash
# Backend (.env.example)
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=your-secret-key-here
SENDGRID_API_KEY=your-sendgrid-key
ENVIRONMENT=development
FRONTEND_URL=http://localhost:3000

# Frontend (.env.example)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Loading Environment Variables**:
```python
# Backend (app/config.py)
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    SENDGRID_API_KEY: str
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
```

```typescript
// Frontend (lib/config.ts)
export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  environment: process.env.NODE_ENV || 'development',
};
```

**Deployment Checklist**:
- [ ] Create `.env.example` with all required variables
- [ ] Add `.env*` to `.gitignore`
- [ ] Set environment variables in Vercel dashboard
- [ ] Set environment variables in Railway dashboard
- [ ] Use different DATABASE_URL for production (Neon)
- [ ] Generate secure SECRET_KEY for production (32+ bytes)
- [ ] Update CORS origins for production domain

**Implementation Notes**:
- Never commit `.env` files
- Use strong secrets in production (not "changeme")
- Rotate secrets periodically
- Document all variables in `.env.example`
- Use platform-specific variable management

**Gotchas to Avoid**:
- Don't commit secrets to git (even in private repos)
- Don't use same secrets for dev/staging/production
- Don't forget to update CORS when deploying
- Don't skip `.env.example` documentation (team onboarding)

---

### Database Migration Execution in Production

**Decision**: Run Alembic migrations as part of deployment process (before starting app)

**Rationale**:
- Ensures database schema matches application code
- Prevents runtime errors from schema mismatches
- Enables zero-downtime deployments (with careful migrations)
- Aligns with GitOps workflow

**Migration Strategy**:
```bash
# In deployment script or Railway start command
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Railway Configuration**:
```toml
# railway.toml
[deploy]
startCommand = "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

**Dockerfile with Migrations**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run migrations then start app
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Zero-Downtime Migration Patterns**:

**Safe Migrations** (can run without downtime):
- Add new table
- Add new column (nullable or with default)
- Add new index (concurrent in PostgreSQL)
- Insert data

**Unsafe Migrations** (require downtime or multi-step deployment):
- Remove column (deploy code first, then remove column)
- Rename column (use multi-step: add new, copy data, remove old)
- Change column type (may lock table)

**Multi-Step Migration Example** (rename column):
```python
# Migration 1: Add new column
def upgrade():
    op.add_column('tasks', sa.Column('task_title', sa.String(200), nullable=True))
    op.execute('UPDATE tasks SET task_title = title')
    op.alter_column('tasks', 'task_title', nullable=False)

# Deploy code that reads from both 'title' and 'task_title'

# Migration 2: Remove old column
def upgrade():
    op.drop_column('tasks', 'title')

# Deploy code that only uses 'task_title'
```

**Migration Rollback**:
```bash
# Rollback last migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision>
```

**Implementation Notes**:
- Always test migrations on staging before production
- Backup database before running migrations
- Use concurrent index creation in PostgreSQL (doesn't lock table)
- Keep migrations small and focused
- Document breaking migrations in migration message

**Gotchas to Avoid**:
- Don't remove columns without multi-step deployment
- Don't run migrations manually in production (automate)
- Don't skip migration testing on staging
- Don't forget to backup database before risky migrations

---

## Summary

This research document provides comprehensive guidance for Phase 2 implementation. Key decisions:

1. **Frontend**: Next.js 14 App Router, Server Components by default, TailwindCSS + shadcn/ui
2. **Backend**: FastAPI with async/await, layered architecture, Pydantic validation
3. **Authentication**: JWT with dual-token pattern, httpOnly cookies + Bearer token support
4. **Database**: Neon PostgreSQL with SQLAlchemy async, Alembic migrations, strategic indexing
5. **Email**: SendGrid with async HTTP client, template-based emails, graceful degradation
6. **API Design**: Versioned endpoints (`/api/v1/`), standardized error responses, CORS support
7. **Testing**: pytest for backend, Vitest for frontend, Playwright for E2E
8. **Deployment**: Vercel for frontend, Railway for backend, automated migrations

All decisions align with the constitution's simplicity principle and Phase 2 scope. Each technology choice is justified and includes implementation patterns, gotchas, and best practices.

**Next Steps**:
1. Review this research document
2. Create Phase 2 specification (`spec.md`) based on these decisions
3. Create Phase 2 implementation plan (`plan.md`)
4. Generate Phase 2 task list (`tasks.md`)
5. Begin implementation following TDD workflow

---

**Document Version**: 1.0
**Last Updated**: 2025-12-07
**Status**: Complete and ready for specification phase
