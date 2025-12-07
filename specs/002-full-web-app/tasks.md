# Implementation Tasks: Phase 2 - Full Web App

**Feature**: Phase 2 - Full Web App
**Branch**: `002-full-web-app`
**Date**: 2025-12-07
**Total Tasks**: 156

## Overview

This document defines all implementation tasks for Phase 2, organized by user story to enable independent development and testing. Each phase represents a complete, shippable increment.

**Task Format**: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- `[P]` = Parallelizable (can run concurrently with other [P] tasks)
- `[Story]` = User story label (US1, US2, etc.)

**Workflow**: Test-Driven Development (TDD) - Write tests → Verify FAIL → Implement → Verify PASS

---

## Phase 1: Setup & Project Initialization (15 tasks)

**Goal**: Initialize project structure for frontend and backend

### Backend Setup

- [ ] T001 [P] Create backend/ directory structure per plan.md (src/, tests/, alembic/)
- [ ] T002 [P] Create backend/requirements.txt with FastAPI, SQLAlchemy, Alembic, PyJWT, bcrypt, psycopg2-binary, sendgrid dependencies
- [ ] T003 [P] Create backend/requirements-dev.txt with pytest, pytest-asyncio, httpx, pytest-cov dependencies
- [ ] T004 [P] Create backend/.env.example with DATABASE_URL, JWT_SECRET_KEY, SENDGRID_API_KEY, CORS_ORIGINS placeholders
- [ ] T005 [P] Create backend/src/config.py to load environment variables using Pydantic BaseSettings
- [ ] T006 [P] Create backend/.gitignore for Python (venv/, __pycache__/, .env, .pytest_cache/)

### Frontend Setup

- [ ] T007 [P] Initialize Next.js 14 project in frontend/ directory with TypeScript and TailwindCSS
- [ ] T008 [P] Create frontend/src directory structure per plan.md (app/, components/, services/, hooks/, types/, utils/)
- [ ] T009 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL placeholder
- [ ] T010 [P] Configure frontend/tsconfig.json with strict mode and path aliases (@/components, @/services, etc.)
- [ ] T011 [P] Configure frontend/tailwind.config.js with custom theme colors and design tokens
- [ ] T012 [P] Create frontend/.gitignore for Node.js (.next/, node_modules/, .env.local)

### Shared Setup

- [ ] T013 [P] Create scripts/migrate-phase1-data.py skeleton with placeholders for JSON → PostgreSQL migration
- [ ] T014 [P] Update root .gitignore to include backend/ and frontend/ specific patterns
- [ ] T015 [P] Create .github/workflows/backend-tests.yml for backend CI (pytest on push)

**Checkpoint**: All directories created, dependencies documented, configuration files in place

---

## Phase 2: Foundational Infrastructure (20 tasks)

**Goal**: Database setup, core models, and shared utilities that block all user stories

**Dependencies**: Must complete Phase 1 (Setup) first

### Database Setup

- [ ] T016 Initialize Alembic in backend/src/db/ with alembic.ini and env.py configured for async SQLAlchemy
- [ ] T017 Create backend/src/db/database.py with SQLAlchemy async engine, session factory, and Base class
- [ ] T018 Create initial Alembic migration 001_initial_schema.py with users, tasks, refresh_tokens tables per data-model.md
- [ ] T019 Create backend/src/db/migrations/env.py to auto-discover models for migrations

### Core Data Models (SQLAlchemy)

- [ ] T020 [P] Create backend/src/models/user.py with User model (id, email, password_hash, display_name, timestamps)
- [ ] T021 [P] Create backend/src/models/task.py with Task model (9 fields per data-model.md including user_id foreign key)
- [ ] T022 [P] Create backend/src/models/refresh_token.py with RefreshToken model (id, user_id, token, expires_at, created_at)
- [ ] T023 Add SQLAlchemy relationships in User model (tasks, refresh_tokens) with cascade deletes

### Pydantic Schemas

- [ ] T024 [P] Create backend/src/schemas/user.py with UserCreate, UserResponse, UserUpdate Pydantic models
- [ ] T025 [P] Create backend/src/schemas/task.py with TaskCreate, TaskUpdate, TaskResponse Pydantic models per Phase 1 schema
- [ ] T026 [P] Create backend/src/schemas/auth.py with LoginRequest, RegisterRequest, TokenResponse, RefreshRequest Pydantic models

### FastAPI App Initialization

- [ ] T027 Create backend/src/main.py with FastAPI app initialization, CORS middleware per research.md
- [ ] T028 Add health check endpoints in backend/src/main.py (GET /health, GET /ready with database connectivity check)
- [ ] T029 Create backend/src/api/dependencies.py with get_db() dependency for database sessions

### Shared Utilities

- [ ] T030 [P] Create backend/src/utils/validators.py migrated from Phase 1 (validate_title, validate_date, validate_priority, validate_title_length, validate_description_length, validate_password_strength)
- [ ] T031 [P] Create backend/src/utils/security.py with bcrypt password hashing functions (hash_password, verify_password)
- [ ] T032 [P] Create frontend/src/types/user.ts with User, LoginRequest, RegisterRequest TypeScript interfaces
- [ ] T033 [P] Create frontend/src/types/task.ts with Task, TaskCreate, TaskUpdate TypeScript interfaces matching Phase 1 schema
- [ ] T034 [P] Create frontend/src/utils/storage.ts with localStorage helpers for JWT token storage (getToken, setToken, removeToken)
- [ ] T035 [P] Create frontend/src/utils/formatters.ts migrated from Phase 1 (formatDate, formatPriority, formatStatus)

**Checkpoint**: Database connected, all models created, shared utilities ready, FastAPI app starts successfully

---

## Phase 3: User Story 1 - User Registration & Authentication (P1) (35 tasks)

**Goal**: Users can register, login, logout, refresh tokens, and reset passwords

**Why this blocks other stories**: Multi-user data isolation requires authentication

**Independent Test Criteria**:
- User can register with email/password and receive confirmation
- User can login and receive JWT access + refresh tokens
- User can access protected endpoint with valid token
- User can refresh expired access token
- User can request password reset and receive email
- User can reset password with valid token

**Dependencies**: Phase 2 (Foundational) must be complete

### Backend: Authentication Service

- [ ] T036 [US1] Create backend/src/services/auth_service.py with generate_jwt_token(user_id, email) function
- [ ] T037 [US1] Add generate_refresh_token(user_id) function to auth_service.py with 7-day expiration
- [ ] T038 [US1] Add verify_jwt_token(token) function to auth_service.py with expiration check
- [ ] T039 [US1] Add create_password_reset_token(user_id) function to auth_service.py with 1-hour expiration
- [ ] T040 [US1] Add verify_password_reset_token(token) function to auth_service.py

### Backend: User Service

- [ ] T041 [US1] Create backend/src/services/user_service.py with async create_user(db, user_create) function
- [ ] T042 [US1] Add async get_user_by_email(db, email) function to user_service.py
- [ ] T043 [US1] Add async get_user_by_id(db, user_id) function to user_service.py
- [ ] T044 [US1] Add async update_user(db, user_id, user_update) function to user_service.py
- [ ] T045 [US1] Add async update_password(db, user_id, new_password_hash) function to user_service.py

### Backend: Email Service (SendGrid)

- [ ] T046 [US1] Create backend/src/services/email_service.py with async send_password_reset_email(to_email, reset_token) function
- [ ] T047 [US1] Add email template for password reset in email_service.py per research.md SendGrid patterns

### Backend: Auth Endpoints

- [ ] T048 [US1] Create backend/src/api/routes/auth.py with POST /api/v1/auth/register endpoint per contracts/api-endpoints.md
- [ ] T049 [US1] Add POST /api/v1/auth/login endpoint to auth.py with email/password validation and token generation
- [ ] T050 [US1] Add POST /api/v1/auth/refresh endpoint to auth.py with refresh token validation
- [ ] T051 [US1] Add POST /api/v1/auth/logout endpoint to auth.py with refresh token revocation
- [ ] T052 [US1] Add POST /api/v1/auth/request-password-reset endpoint to auth.py per contracts/api-endpoints.md
- [ ] T053 [US1] Add POST /api/v1/auth/reset-password endpoint to auth.py with token validation

### Backend: Auth Middleware & Dependencies

- [ ] T054 [US1] Create backend/src/api/dependencies.py get_current_user() dependency with JWT validation
- [ ] T055 [US1] Add rate limiting middleware in backend/src/middleware/rate_limiter.py (100 req/min auth endpoints)

### Backend: Tests for US1

- [ ] T056 [P] [US1] Create backend/tests/conftest.py with test database fixture (in-memory SQLite) and test client fixture
- [ ] T057 [P] [US1] Create backend/tests/unit/test_auth_service.py with tests for JWT generation/verification
- [ ] T058 [P] [US1] Create backend/tests/unit/test_user_service.py with tests for user CRUD operations
- [ ] T059 [P] [US1] Create backend/tests/integration/test_auth_endpoints.py with registration, login, refresh, logout tests
- [ ] T060 [US1] Run backend tests: pytest backend/tests/ -k US1 -v (expect ALL PASS)

### Frontend: Auth Service & API Client

- [ ] T061 [P] [US1] Create frontend/src/services/api.ts with axios instance configured for base URL and auth interceptors
- [ ] T062 [P] [US1] Create frontend/src/services/authService.ts with register(email, password, displayName) API call
- [ ] T063 [P] [US1] Add login(email, password) function to authService.ts
- [ ] T064 [P] [US1] Add logout() function to authService.ts
- [ ] T065 [P] [US1] Add refreshToken(refreshToken) function to authService.ts with automatic retry on 401
- [ ] T066 [P] [US1] Add requestPasswordReset(email) function to authService.ts
- [ ] T067 [P] [US1] Add resetPassword(token, newPassword) function to authService.ts

### Frontend: Auth Context & Hooks

- [ ] T068 [US1] Create frontend/src/hooks/useAuth.tsx with AuthContext providing user state, login, logout, register functions
- [ ] T069 [US1] Add token refresh logic to useAuth.tsx with automatic renewal before expiration

### Frontend: Auth Pages

- [ ] T070 [P] [US1] Create frontend/src/app/login/page.tsx with email/password form and validation
- [ ] T071 [P] [US1] Create frontend/src/app/register/page.tsx with email/password/name form per acceptance criteria
- [ ] T072 [P] [US1] Create frontend/src/app/reset-password/page.tsx with email submission form
- [ ] T073 [P] [US1] Create frontend/src/app/reset-password/[token]/page.tsx with new password form

### Frontend: Auth Components

- [ ] T074 [P] [US1] Create frontend/src/components/AuthForm.tsx reusable component for login/register forms
- [ ] T075 [P] [US1] Create frontend/src/components/ProtectedRoute.tsx wrapper to guard authenticated routes

### Frontend: Tests for US1

- [ ] T076 [P] [US1] Create frontend/tests/unit/authService.test.ts with API call mocking tests
- [ ] T077 [P] [US1] Create frontend/tests/e2e/auth.spec.ts with Playwright tests for registration → login → logout flow
- [ ] T078 [US1] Run frontend tests: npm run test -- auth (expect ALL PASS)

### Integration Validation for US1

- [ ] T079 [US1] Manual test: Register new user via frontend, verify user in database, verify JWT token works
- [ ] T080 [US1] Manual test: Login with registered user, verify token refresh works, verify logout clears tokens
- [ ] T081 [US1] Manual test: Request password reset, verify email received (check SendGrid logs), reset password successfully

**Phase 3 Checkpoint**: ✅ Authentication complete, users can register/login/logout, tokens work, password reset functional

---

## Phase 4: User Story 2 - Web-Based Task Management (P2) (32 tasks)

**Goal**: Authenticated users can perform all task CRUD operations via web UI

**Why this priority**: Core value proposition, migrates Phase 1 CLI to web

**Independent Test Criteria**:
- Logged-in user can create task with all Phase 1 fields (title, description, priority, due_date)
- User can view list of their tasks (filtered by user_id)
- User can edit any task field
- User can mark task as complete
- User can delete task
- User can filter by status and priority
- All operations isolated to authenticated user (data isolation test)

**Dependencies**: Phase 3 (US1 Authentication) must be complete

### Backend: Task Service

- [ ] T082 [P] [US2] Create backend/src/services/task_service.py with async create_task(db, user_id, task_create) function
- [ ] T083 [P] [US2] Add async get_tasks(db, user_id, status=None, priority=None, sort_by='created_at', order='desc', limit=50, offset=0) function per contracts/api-endpoints.md
- [ ] T084 [P] [US2] Add async get_task_by_id(db, task_id, user_id) function with ownership validation
- [ ] T085 [P] [US2] Add async update_task(db, task_id, user_id, task_update) function with ownership check
- [ ] T086 [P] [US2] Add async delete_task(db, task_id, user_id) function with ownership check
- [ ] T087 [P] [US2] Add async complete_task(db, task_id, user_id) helper function to mark status as completed

### Backend: Task Endpoints

- [ ] T088 [US2] Create backend/src/api/routes/tasks.py with GET /api/v1/tasks endpoint supporting filters per contracts/api-endpoints.md
- [ ] T089 [US2] Add POST /api/v1/tasks endpoint to tasks.py with current_user dependency
- [ ] T090 [US2] Add GET /api/v1/tasks/{task_id} endpoint to tasks.py with ownership validation
- [ ] T091 [US2] Add PUT /api/v1/tasks/{task_id} endpoint to tasks.py with partial update support
- [ ] T092 [US2] Add DELETE /api/v1/tasks/{task_id} endpoint to tasks.py returning 204 No Content

### Backend: Tests for US2

- [ ] T093 [P] [US2] Create backend/tests/unit/test_task_service.py with tests for CRUD operations and filtering
- [ ] T094 [P] [US2] Create backend/tests/integration/test_task_endpoints.py with full CRUD flow test and data isolation test
- [ ] T095 [US2] Run backend tests: pytest backend/tests/ -k US2 -v (expect ALL PASS)

### Frontend: Task Service

- [ ] T096 [P] [US2] Create frontend/src/services/taskService.ts with getTasks(filters?) API call
- [ ] T097 [P] [US2] Add createTask(taskCreate) function to taskService.ts
- [ ] T098 [P] [US2] Add getTask(taskId) function to taskService.ts
- [ ] T099 [P] [US2] Add updateTask(taskId, taskUpdate) function to taskService.ts
- [ ] T100 [P] [US2] Add deleteTask(taskId) function to taskService.ts

### Frontend: Task State Management

- [ ] T101 [US2] Create frontend/src/hooks/useTasks.tsx with task list state, CRUD operations, and filter state
- [ ] T102 [US2] Add optimistic updates to useTasks.tsx for create/update/delete operations

### Frontend: Task Components

- [ ] T103 [P] [US2] Create frontend/src/components/TaskList.tsx displaying tasks with filter controls per acceptance criteria
- [ ] T104 [P] [US2] Create frontend/src/components/TaskItem.tsx for individual task display with edit/delete/complete actions
- [ ] T105 [P] [US2] Create frontend/src/components/TaskForm.tsx for add/edit task modal with validation per Phase 1 constraints
- [ ] T106 [P] [US2] Create frontend/src/components/TaskFilters.tsx for status/priority filtering UI

### Frontend: Dashboard Page

- [ ] T107 [US2] Create frontend/src/app/dashboard/page.tsx as main task management interface with TaskList and TaskForm
- [ ] T108 [US2] Add empty state UI to dashboard page per edge cases in spec.md ("Add your first task" CTA)
- [ ] T109 [US2] Add responsive design to dashboard using TailwindCSS breakpoints per acceptance criteria

### Frontend: Tests for US2

- [ ] T110 [P] [US2] Create frontend/tests/unit/components/TaskList.test.tsx with rendering and filter tests
- [ ] T111 [P] [US2] Create frontend/tests/e2e/tasks.spec.ts with Playwright tests for full CRUD flow
- [ ] T112 [US2] Run frontend tests: npm run test -- tasks (expect ALL PASS)

### Integration Validation for US2

- [ ] T113 [US2] Manual test: Login, create task, verify appears in list, edit task, verify changes saved
- [ ] T114 [US2] Manual test: Mark task complete, verify status change, delete task, verify removed
- [ ] T115 [US2] Manual test: Create tasks with different priorities/statuses, verify filters work correctly
- [ ] T116 [US2] Manual test: Login as two different users, verify tasks are isolated (User A cannot see User B's tasks)

**Phase 4 Checkpoint**: ✅ Task management complete, all CRUD operations work, data isolation verified

---

## Phase 5: User Story 3 - Real-Time Task Sync (P3) (18 tasks)

**Goal**: Tasks sync across devices/tabs in real-time without manual refresh

**Why this priority**: Enhances UX but not critical for MVP

**Independent Test Criteria**:
- Open app in two browser tabs
- Create task in tab A, see it appear in tab B within 2 seconds (no refresh)
- Complete task in tab B, see status update in tab A
- Test offline changes sync when reconnecting

**Dependencies**: Phase 4 (US2 Task Management) must be complete

### Backend: WebSocket Support (Optional Approach 1)

- [ ] T117 [P] [US3] Research: Decide between WebSocket (FastAPI WebSocket) vs. Polling (short polling every 5s) per research.md real-time patterns
- [ ] T118 [US3] If WebSocket chosen: Add fastapi-websocket dependency to backend/requirements.txt
- [ ] T119 [US3] If WebSocket chosen: Create backend/src/api/routes/websocket.py with /ws endpoint for task updates
- [ ] T120 [US3] If WebSocket chosen: Implement task update broadcasting in task_service.py after create/update/delete operations

### Frontend: Real-Time Sync (Polling Approach - Simpler)

- [ ] T121 [P] [US3] Add polling logic to frontend/src/hooks/useTasks.tsx to refetch tasks every 5 seconds when tab is active
- [ ] T122 [P] [US3] Add visibility change detection to useTasks.tsx to pause polling when tab inactive
- [ ] T123 [P] [US3] Implement optimistic UI updates with server reconciliation in useTasks.tsx

### Frontend: Real-Time Sync (WebSocket Approach - If Chosen)

- [ ] T124 [P] [US3] If WebSocket: Create frontend/src/services/websocketService.ts with connection management
- [ ] T125 [P] [US3] If WebSocket: Integrate websocketService into useTasks.tsx to receive real-time updates
- [ ] T126 [US3] If WebSocket: Add reconnection logic with exponential backoff in websocketService.ts

### Offline Support

- [ ] T127 [P] [US3] Add offline detection to frontend/src/hooks/useOnlineStatus.tsx
- [ ] T128 [P] [US3] Queue offline changes in useTasks.tsx using localStorage
- [ ] T129 [US3] Implement sync-on-reconnect logic in useTasks.tsx to send queued changes when back online

### Tests for US3

- [ ] T130 [P] [US3] Create frontend/tests/e2e/realtime-sync.spec.ts with two-tab sync test using Playwright
- [ ] T131 [US3] Run frontend tests: npm run test -- realtime (expect ALL PASS)

### Integration Validation for US3

- [ ] T132 [US3] Manual test: Open two browser tabs, create task in tab 1, verify appears in tab 2 within 5 seconds
- [ ] T133 [US3] Manual test: Disable network, create task, enable network, verify task syncs
- [ ] T134 [US3] Manual test: Complete task in one tab, verify status updates in other tab

**Phase 5 Checkpoint**: ✅ Real-time sync working, tasks appear across devices within 2-5 seconds

---

## Phase 6: User Story 4 - User Profile & Preferences (P4) (12 tasks)

**Goal**: Users can manage account settings and preferences

**Why this priority**: Personalization feature, not essential for core functionality

**Independent Test Criteria**:
- User can access profile settings page
- User can update display name and see change throughout app
- User can change password and login with new password
- User can toggle dark mode and preference persists

**Dependencies**: Phase 3 (US1 Authentication) must be complete

### Backend: User Profile Endpoints

- [ ] T135 [US4] Add GET /api/v1/users/me endpoint to backend/src/api/routes/users.py returning current user profile
- [ ] T136 [US4] Add PUT /api/v1/users/me endpoint to users.py for updating display_name and email
- [ ] T137 [US4] Add PUT /api/v1/users/me/password endpoint to users.py for password change with current password validation

### Backend: Tests for US4

- [ ] T138 [P] [US4] Create backend/tests/integration/test_user_endpoints.py with profile update and password change tests
- [ ] T139 [US4] Run backend tests: pytest backend/tests/ -k US4 -v (expect ALL PASS)

### Frontend: User Profile Service

- [ ] T140 [P] [US4] Add getCurrentUser() function to frontend/src/services/authService.ts
- [ ] T141 [P] [US4] Add updateProfile(displayName, email) function to authService.ts
- [ ] T142 [P] [US4] Add changePassword(currentPassword, newPassword) function to authService.ts

### Frontend: Profile Page & Preferences

- [ ] T143 [US4] Create frontend/src/app/profile/page.tsx with display name and email update form
- [ ] T144 [US4] Add password change section to profile page with current/new password fields
- [ ] T145 [US4] Create frontend/src/hooks/useTheme.tsx for dark mode toggle with localStorage persistence
- [ ] T146 [US4] Add dark mode toggle to frontend/src/components/Header.tsx with theme switching

### Integration Validation for US4

- [ ] T147 [US4] Manual test: Update display name, verify appears in header and profile page
- [ ] T148 [US4] Manual test: Change password, logout, login with new password successfully
- [ ] T149 [US4] Manual test: Toggle dark mode, verify theme changes, refresh page, verify preference persists

**Phase 6 Checkpoint**: ✅ User profile management complete, preferences persist

---

## Phase 7: User Story 5 - Task Search & Advanced Filtering (P5) (10 tasks)

**Goal**: Power users can search and filter large task lists efficiently

**Why this priority**: Nice-to-have for power users with many tasks

**Independent Test Criteria**:
- User with 50+ tasks can search by keyword and see results in <1 second
- User can filter by date range (e.g., "due this week")
- User can combine multiple filters (status + priority + date range)

**Dependencies**: Phase 4 (US2 Task Management) must be complete

### Backend: Advanced Search & Filtering

- [ ] T150 [US5] Add full-text search support to backend/src/services/task_service.py get_tasks() function with query parameter
- [ ] T151 [US5] Add date range filtering (due_date_start, due_date_end) to get_tasks() function
- [ ] T152 [US5] Add database index on tasks.title for search performance in Alembic migration

### Frontend: Search & Advanced Filters

- [ ] T153 [P] [US5] Create frontend/src/components/TaskSearch.tsx with real-time search input
- [ ] T154 [P] [US5] Add date range picker to frontend/src/components/TaskFilters.tsx
- [ ] T155 [US5] Integrate search and filters into frontend/src/hooks/useTasks.tsx with debouncing

### Tests for US5

- [ ] T156 [P] [US5] Create backend/tests/integration/test_search.py with search performance test (50+ tasks, <1s response)
- [ ] T157 [US5] Run backend tests: pytest backend/tests/ -k US5 -v (expect ALL PASS)

### Integration Validation for US5

- [ ] T158 [US5] Manual test: Create 50 tasks, search by keyword, verify results appear in <1 second
- [ ] T159 [US5] Manual test: Apply date range filter (due this week), verify only matching tasks shown

**Phase 7 Checkpoint**: ✅ Advanced search and filtering complete, fast performance verified

---

## Final Phase: Polish & Cross-Cutting Concerns (16 tasks)

**Goal**: Production readiness, performance, security, deployment

**Dependencies**: All user story phases (US1-US5) complete

### Security Hardening

- [ ] T160 [P] Add input sanitization middleware to backend/src/middleware/security.py to prevent XSS
- [ ] T161 [P] Add SQL injection protection audit (verify all queries use parameterized statements)
- [ ] T162 [P] Add CSRF protection for state-changing requests in backend/src/middleware/csrf.py
- [ ] T163 [P] Add security headers (X-Content-Type-Options, X-Frame-Options, etc.) to FastAPI middleware

### Performance Optimization

- [ ] T164 [P] Add database connection pooling configuration to backend/src/db/database.py per research.md (5-20 connections)
- [ ] T165 [P] Add response caching for GET /api/v1/tasks with cache invalidation on updates
- [ ] T166 [P] Optimize frontend bundle size (analyze with next build && next analyze, target <500KB gzipped)
- [ ] T167 [P] Add lazy loading for task list pagination in frontend/src/components/TaskList.tsx

### Error Handling & Logging

- [ ] T168 [P] Create backend/src/middleware/error_handler.py with standardized error response format per contracts/api-endpoints.md
- [ ] T169 [P] Add structured JSON logging to backend/src/utils/logger.py with correlation IDs
- [ ] T170 [P] Add error boundary to frontend/src/app/layout.tsx for graceful error handling
- [ ] T171 [P] Add frontend error logging service in frontend/src/services/errorService.ts

### Deployment Preparation

- [ ] T172 Create backend/Dockerfile for FastAPI deployment to Railway/Render
- [ ] T173 Create frontend/next.config.js optimizations for Vercel deployment
- [ ] T174 Document deployment steps in specs/002-full-web-app/deployment.md with environment setup

### Final Validation

- [ ] T175 Run full test suite: pytest backend/tests/ -v && npm run test (expect ALL PASS)
- [ ] T176 Run Playwright E2E tests across all user stories: npm run test:e2e (expect ALL PASS)

**Final Phase Checkpoint**: ✅ Production-ready, all tests passing, deployment documented

---

## Task Summary

**Total Tasks**: 176 tasks

**By Phase**:
- Phase 1 (Setup): 15 tasks
- Phase 2 (Foundational): 20 tasks
- Phase 3 (US1 - Authentication): 46 tasks
- Phase 4 (US2 - Task Management): 35 tasks
- Phase 5 (US3 - Real-Time Sync): 18 tasks
- Phase 6 (US4 - User Profile): 15 tasks
- Phase 7 (US5 - Search & Filtering): 11 tasks
- Final Phase (Polish): 16 tasks

**By User Story**:
- US1 (Authentication): 46 tasks
- US2 (Task Management): 35 tasks
- US3 (Real-Time Sync): 18 tasks
- US4 (User Profile): 15 tasks
- US5 (Search & Filtering): 11 tasks
- Infrastructure: 51 tasks (Setup + Foundational + Polish)

**Parallelization Opportunities**: 68 tasks marked with [P] can run concurrently

---

## Dependencies & Execution Order

**User Story Dependencies**:

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← BLOCKS all user stories
    ↓
    ├──→ Phase 3 (US1) ← BLOCKS US2, US3, US4, US5 (authentication required)
    │         ↓
    │    Phase 4 (US2) ← BLOCKS US3, US5 (task management required)
    │         ↓
    │    ├──→ Phase 5 (US3) [Independent after US2]
    │    └──→ Phase 7 (US5) [Independent after US2]
    │
    └──→ Phase 6 (US4) [Independent after US1]

    After all phases complete:
    ↓
Final Phase (Polish)
```

**Critical Path**: Setup → Foundational → US1 → US2 → (US3 or US5) → Polish

**Parallel Paths**:
- US4 can be developed in parallel with US2 (both depend only on US1)
- US3 and US5 can be developed in parallel (both depend on US2)

---

## Parallel Execution Examples

### Phase 3 (US1) Parallel Opportunities

**Can run concurrently** (no dependencies):
- T036-T040 (auth_service.py functions)
- T041-T045 (user_service.py functions)
- T046-T047 (email_service.py)
- T056-T059 (backend tests)
- T061-T067 (frontend authService.ts)
- T070-T075 (frontend pages and components)

**Sequential** (dependencies):
- T054 (get_current_user dependency) requires T036-T040 (JWT functions) complete first
- T048-T053 (auth endpoints) require T036-T047 (services) complete first
- T068-T069 (useAuth hook) require T061-T067 (authService) complete first

### Phase 4 (US2) Parallel Opportunities

**Can run concurrently**:
- T082-T087 (task_service.py functions)
- T093-T094 (backend tests)
- T096-T100 (frontend taskService.ts)
- T103-T106 (frontend components)

**Sequential**:
- T088-T092 (task endpoints) require T082-T087 (task_service) complete first
- T101-T102 (useTasks hook) require T096-T100 (taskService) complete first
- T107-T109 (dashboard page) require T101-T106 (hooks and components) complete first

---

## MVP Scope Recommendation

**Minimum Viable Product** (first shippable increment):

**Include**:
- ✅ Phase 1: Setup
- ✅ Phase 2: Foundational
- ✅ Phase 3: User Story 1 (Authentication)
- ✅ Phase 4: User Story 2 (Task Management)
- ✅ Selected polish tasks: T160-T163 (security), T168-T171 (error handling)

**Defer to v2**:
- ⏸️ Phase 5: User Story 3 (Real-Time Sync) - nice to have
- ⏸️ Phase 6: User Story 4 (User Profile) - nice to have
- ⏸️ Phase 7: User Story 5 (Advanced Search) - nice to have
- ⏸️ Remaining polish tasks

**MVP Rationale**: US1 + US2 deliver core value (multi-user web-based task management). This validates Phase 1 → Phase 2 migration and provides shippable product for user feedback before investing in advanced features.

**MVP Task Count**: 111 tasks (63% of total)

---

## Implementation Strategy

### Test-Driven Development (TDD) Workflow

**For each user story**:

1. **Write tests FIRST** (tasks with test files)
2. **Run tests** → Verify they FAIL (expected behavior)
3. **Implement functionality** (implementation tasks)
4. **Run tests** → Verify they PASS
5. **Checkpoint validation** before next story

**Example for US1**:
1. Tasks T056-T059: Write all authentication tests (registration, login, token refresh, etc.)
2. Run `pytest backend/tests/ -k US1` → expect FAIL (not implemented yet)
3. Tasks T036-T055: Implement authentication services and endpoints
4. Run `pytest backend/tests/ -k US1` → expect PASS (all green)
5. Checkpoint: Authentication complete, move to US2

### Incremental Delivery

**Week 1-2**: MVP (US1 + US2)
- Setup + Foundational + Authentication + Task Management
- Deliverable: Working multi-user task management web app

**Week 3**: Real-Time & Profile (US3 + US4)
- Deliverable: Enhanced UX with sync and personalization

**Week 4**: Search & Polish (US5 + Final)
- Deliverable: Production-ready with advanced features

### Checkpoint Validation

**After each phase**:
- ✅ All tests passing for that phase
- ✅ Manual smoke test of acceptance scenarios
- ✅ Code review (if team environment)
- ✅ Git commit with descriptive message
- ✅ Update CLAUDE.md with progress

**Phase Completion Criteria**:
- All tasks in phase checkbox marked `[X]`
- Pytest/Vitest tests 100% passing for that phase
- Manual validation of independent test criteria passed
- No regressions in previous phases

---

**Tasks.md Complete**: 2025-12-07
**Ready for Implementation**: Run `/sp.implement` to execute TDD workflow
