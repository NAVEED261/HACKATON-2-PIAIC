# API Endpoints: Phase 2 - Full Web App

**Feature**: Phase 2 - Full Web App
**Date**: 2025-12-07
**API Version**: v1
**Base URL**: `http://localhost:8000/api/v1` (development) | `https://api.yourdomain.com/api/v1` (production)

## Overview

This document defines the RESTful API endpoints for Phase 2, covering authentication, task management, and user profile operations. All endpoints follow REST conventions, return JSON responses, and use JWT Bearer authentication (except public auth endpoints).

**API Design Principles**:
- RESTful resource-oriented URLs
- Standard HTTP methods (GET, POST, PUT, DELETE)
- JWT Bearer token authentication
- Consistent error response format
- API versioning via URL path (`/api/v1/`)

---

## Authentication Endpoints

### POST /api/v1/auth/register

**Purpose**: Register a new user account

**Authentication**: None (public endpoint)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "display_name": "John Doe"
}
```

**Request Schema**:
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `email` | string | Yes | Valid email format, max 255 chars, unique |
| `password` | string | Yes | Min 8 chars, 1 uppercase, 1 lowercase, 1 digit (FR-008) |
| `display_name` | string | Yes | 1-100 chars, no leading/trailing whitespace |

**Success Response** (201 Created):
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "display_name": "John Doe",
    "created_at": "2025-12-07T10:30:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input (weak password, invalid email)
  ```json
  {
    "error": "validation_error",
    "message": "Password must contain at least 1 uppercase letter",
    "details": {"field": "password"}
  }
  ```
- `409 Conflict`: Email already registered
  ```json
  {
    "error": "email_already_exists",
    "message": "An account with this email already exists"
  }
  ```

---

### POST /api/v1/auth/login

**Purpose**: Authenticate user and receive JWT tokens

**Authentication**: None (public endpoint)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Request Schema**:
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `email` | string | Yes | Valid email format |
| `password` | string | Yes | Any string (validation happens server-side) |

**Success Response** (200 OK):
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "display_name": "John Doe",
    "created_at": "2025-12-07T10:30:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Token Details**:
- **access_token**: Expires in 24 hours (FR-004)
- **refresh_token**: Expires in 7 days (FR-006), stored in database

**Error Responses**:
- `401 Unauthorized`: Invalid credentials
  ```json
  {
    "error": "invalid_credentials",
    "message": "Email or password is incorrect"
  }
  ```
- `429 Too Many Requests`: Rate limit exceeded (100 requests/min per IP, FR-024)
  ```json
  {
    "error": "rate_limit_exceeded",
    "message": "Too many login attempts. Try again in 60 seconds."
  }
  ```

---

### POST /api/v1/auth/refresh

**Purpose**: Obtain new access token using refresh token

**Authentication**: Refresh token in request body

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or expired refresh token
  ```json
  {
    "error": "invalid_refresh_token",
    "message": "Refresh token is invalid or expired"
  }
  ```

---

### POST /api/v1/auth/logout

**Purpose**: Revoke refresh token (client should also delete stored tokens)

**Authentication**: Required (Bearer token)

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response** (200 OK):
```json
{
  "message": "Logged out successfully"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid access token

---

### POST /api/v1/auth/request-password-reset

**Purpose**: Send password reset email (FR-005)

**Authentication**: None (public endpoint)

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Success Response** (200 OK):
```json
{
  "message": "If an account with that email exists, a password reset link has been sent"
}
```

**Note**: Always returns success (200) even if email doesn't exist, to prevent user enumeration attacks.

**Email Content**:
- Subject: "Reset Your Password"
- Body: Contains reset link with token (expires in 1 hour)
- Link format: `https://app.yourdomain.com/reset-password?token={token}`

**Error Responses**:
- `429 Too Many Requests`: Rate limit (5 requests per email per hour)

---

### POST /api/v1/auth/reset-password

**Purpose**: Complete password reset with token from email

**Authentication**: None (token in request body)

**Request Body**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "new_password": "NewSecurePassword123"
}
```

**Success Response** (200 OK):
```json
{
  "message": "Password reset successfully"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid token or weak password
- `401 Unauthorized`: Expired token

---

## Task Management Endpoints

### GET /api/v1/tasks

**Purpose**: List authenticated user's tasks with optional filters (FR-009, FR-015)

**Authentication**: Required (Bearer token)

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | string | No | all | Filter by status: `pending`, `completed`, `all` |
| `priority` | string | No | all | Filter by priority: `low`, `medium`, `high`, `all` |
| `sort_by` | string | No | `created_at` | Sort field: `created_at`, `due_date`, `priority` |
| `order` | string | No | `desc` | Sort order: `asc`, `desc` |
| `limit` | integer | No | 50 | Max results (1-100) |
| `offset` | integer | No | 0 | Pagination offset |

**Example Request**:
```
GET /api/v1/tasks?status=pending&priority=high&sort_by=due_date&order=asc
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project proposal",
      "description": "Draft and submit Q1 proposal",
      "status": "pending",
      "priority": "high",
      "due_date": "2025-12-15",
      "created_at": "2025-12-07T10:30:00Z",
      "updated_at": "2025-12-07T10:30:00Z"
    },
    {
      "id": 2,
      "title": "Review PR #42",
      "description": null,
      "status": "pending",
      "priority": "medium",
      "due_date": null,
      "created_at": "2025-12-06T14:20:00Z",
      "updated_at": "2025-12-06T14:20:00Z"
    }
  ],
  "total": 2,
  "limit": 50,
  "offset": 0
}
```

**Response Schema**:
- `tasks`: Array of task objects (filtered by `user_id = current_user.id`)
- `total`: Total matching tasks (for pagination)
- `limit`: Applied limit
- `offset`: Applied offset

**Error Responses**:
- `401 Unauthorized`: Missing or invalid access token
- `400 Bad Request`: Invalid query parameters

---

### POST /api/v1/tasks

**Purpose**: Create a new task for authenticated user (FR-009)

**Authentication**: Required (Bearer token)

**Request Body**:
```json
{
  "title": "Complete project proposal",
  "description": "Draft and submit Q1 proposal",
  "priority": "high",
  "due_date": "2025-12-15"
}
```

**Request Schema**:
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `title` | string | Yes | 1-200 chars |
| `description` | string | No | Max 1000 chars |
| `priority` | string | No | Enum: `low`, `medium`, `high` (default: `medium`) |
| `due_date` | string | No | ISO 8601 YYYY-MM-DD format, cannot be in past |

**Success Response** (201 Created):
```json
{
  "id": 3,
  "title": "Complete project proposal",
  "description": "Draft and submit Q1 proposal",
  "status": "pending",
  "priority": "high",
  "due_date": "2025-12-15",
  "created_at": "2025-12-07T11:00:00Z",
  "updated_at": "2025-12-07T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid access token
- `400 Bad Request`: Validation errors (title too long, invalid due_date, etc.)

---

### GET /api/v1/tasks/{task_id}

**Purpose**: Retrieve a single task by ID

**Authentication**: Required (Bearer token)

**Path Parameters**:
- `task_id`: integer (task ID)

**Success Response** (200 OK):
```json
{
  "id": 1,
  "title": "Complete project proposal",
  "description": "Draft and submit Q1 proposal",
  "status": "pending",
  "priority": "high",
  "due_date": "2025-12-15",
  "created_at": "2025-12-07T10:30:00Z",
  "updated_at": "2025-12-07T10:30:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid access token
- `404 Not Found`: Task doesn't exist or doesn't belong to authenticated user
  ```json
  {
    "error": "task_not_found",
    "message": "Task not found"
  }
  ```

---

### PUT /api/v1/tasks/{task_id}

**Purpose**: Update an existing task (FR-011)

**Authentication**: Required (Bearer token)

**Path Parameters**:
- `task_id`: integer (task ID)

**Request Body** (partial updates allowed):
```json
{
  "title": "Updated project proposal",
  "description": "Draft, review, and submit Q1 proposal",
  "priority": "medium",
  "due_date": "2025-12-20",
  "status": "completed"
}
```

**Request Schema**:
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `title` | string | No | 1-200 chars if provided |
| `description` | string | No | Max 1000 chars if provided |
| `priority` | string | No | Enum: `low`, `medium`, `high` |
| `due_date` | string | No | ISO 8601 YYYY-MM-DD format, cannot be in past |
| `status` | string | No | Enum: `pending`, `completed` |

**Success Response** (200 OK):
```json
{
  "id": 1,
  "title": "Updated project proposal",
  "description": "Draft, review, and submit Q1 proposal",
  "status": "completed",
  "priority": "medium",
  "due_date": "2025-12-20",
  "created_at": "2025-12-07T10:30:00Z",
  "updated_at": "2025-12-07T15:45:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid access token
- `404 Not Found`: Task doesn't exist or doesn't belong to authenticated user
- `400 Bad Request`: Validation errors

---

### DELETE /api/v1/tasks/{task_id}

**Purpose**: Delete a task (FR-012)

**Authentication**: Required (Bearer token)

**Path Parameters**:
- `task_id`: integer (task ID)

**Success Response** (204 No Content):
- Empty response body

**Error Responses**:
- `401 Unauthorized`: Missing or invalid access token
- `404 Not Found`: Task doesn't exist or doesn't belong to authenticated user

---

## User Profile Endpoints

### GET /api/v1/users/me

**Purpose**: Retrieve authenticated user's profile

**Authentication**: Required (Bearer token)

**Success Response** (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "display_name": "John Doe",
  "created_at": "2025-12-07T10:30:00Z",
  "updated_at": "2025-12-07T10:30:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid access token

---

### PUT /api/v1/users/me

**Purpose**: Update authenticated user's profile (FR-014)

**Authentication**: Required (Bearer token)

**Request Body** (partial updates allowed):
```json
{
  "display_name": "Jane Doe",
  "email": "newemail@example.com"
}
```

**Request Schema**:
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `display_name` | string | No | 1-100 chars if provided |
| `email` | string | No | Valid email format, unique if provided |

**Success Response** (200 OK):
```json
{
  "id": 1,
  "email": "newemail@example.com",
  "display_name": "Jane Doe",
  "created_at": "2025-12-07T10:30:00Z",
  "updated_at": "2025-12-07T16:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid access token
- `400 Bad Request`: Validation errors
- `409 Conflict`: Email already in use by another user

---

## Health Check Endpoints

### GET /health

**Purpose**: Basic health check (for load balancers)

**Authentication**: None (public endpoint)

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

### GET /ready

**Purpose**: Readiness check (includes database connectivity)

**Authentication**: None (public endpoint)

**Success Response** (200 OK):
```json
{
  "status": "ready",
  "database": "connected",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

**Error Response** (503 Service Unavailable):
```json
{
  "status": "not_ready",
  "database": "disconnected",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

## Error Response Format

All error responses follow this standardized format:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {
    "field": "additional context (optional)"
  }
}
```

**Common Error Codes**:
- `validation_error`: Request validation failed
- `invalid_credentials`: Login failed
- `unauthorized`: Missing or invalid access token
- `forbidden`: User doesn't have permission
- `not_found`: Resource doesn't exist
- `email_already_exists`: Email conflict during registration
- `rate_limit_exceeded`: Too many requests

---

## Authentication Flow

### Standard Request Authentication

All protected endpoints require the `Authorization` header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**JWT Token Structure**:
```json
{
  "sub": 1,              // User ID
  "email": "user@example.com",
  "exp": 1702134600,     // Expiration timestamp (24h from issue)
  "iat": 1702048200      // Issued at timestamp
}
```

### Token Refresh Flow

1. Client receives `access_token` (24h expiry) and `refresh_token` (7d expiry) on login
2. Client stores both tokens securely
3. When access token expires (401 response), client calls `/auth/refresh` with refresh token
4. Server validates refresh token and issues new access token
5. Client retries original request with new access token

---

## Rate Limiting

**Rate Limits** (FR-024):
- Auth endpoints: 100 requests/minute per IP
- Other endpoints: 1000 requests/minute per authenticated user

**Rate Limit Headers** (included in all responses):
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1702048800
```

**429 Response** (rate limit exceeded):
```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Try again in 42 seconds.",
  "retry_after": 42
}
```

---

## CORS Configuration

**Allowed Origins** (configurable via environment):
- Development: `http://localhost:3000`
- Production: `https://yourdomain.com`

**Allowed Headers**:
- `Authorization`
- `Content-Type`

**Allowed Methods**:
- `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`

**Credentials**: Enabled (allows cookies/auth headers)

---

## Versioning Strategy

**Current Version**: v1

**URL Format**: `/api/v1/endpoint`

**Future Versions**:
- Breaking changes will increment version: `/api/v2/endpoint`
- Non-breaking changes (new fields, new endpoints) can be added to v1
- Old versions supported for minimum 6 months after new version release

---

**API Contracts Complete**: 2025-12-07
**Next Step**: Generate OpenAPI 3.0 specification (`contracts/openapi.yaml`)
