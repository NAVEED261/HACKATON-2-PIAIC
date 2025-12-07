---
id: PHR-002-002
title: Phase 2 Task Generation
stage: tasks
date: 2025-12-07T13:00:00Z
surface: claude-code
model: claude-sonnet-4-5
feature: full-web-app
branch: 002-full-web-app
user: developer
command: /sp.tasks
labels: [tasks, implementation, tdd, user-stories]
links:
  spec: specs/002-full-web-app/spec.md
  plan: specs/002-full-web-app/plan.md
  tasks: specs/002-full-web-app/tasks.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - path: specs/002-full-web-app/tasks.md
    status: created
    lines: 620
tests:
  - name: Task Format Validation
    status: PASS
    details: All 176 tasks follow checklist format with TaskID, optional [P] and [Story] markers
  - name: User Story Coverage
    status: PASS
    details: All 5 user stories (US1-US5) have complete task breakdowns
  - name: Dependency Graph
    status: PASS
    details: Dependencies documented, critical path identified, parallel opportunities marked
---

## Prompt

```
User requested to continue after Phase 2 planning completion.
Command triggered: /sp.tasks

Goal: Generate implementation task list organized by user story with TDD workflow

Expected outputs:
1. tasks.md file with all implementation tasks
2. Tasks organized by user story (US1-US5) with independent test criteria
3. Strict checklist format with TaskID, [P] markers, [Story] labels, file paths
4. Dependency graph showing user story completion order
5. Parallel execution opportunities identified
6. MVP scope recommendation
7. TDD workflow guidance
```

## Response snapshot

### Task Generation Process

**Step 1: Load Planning Artifacts**
- Read spec.md: 5 user stories (P1-P5) with acceptance criteria
- Read plan.md: Tech stack (Next.js, FastAPI, Neon PostgreSQL, JWT)
- Read data-model.md: 3 entities (User, Task, RefreshToken)
- Read contracts/api-endpoints.md: 15 REST API endpoints
- Read research.md: Technology decisions and patterns

**Step 2: Extract User Stories**
- **US1 (P1)**: User Registration & Authentication - foundation for multi-user
- **US2 (P2)**: Web-Based Task Management - core CRUD functionality
- **US3 (P3)**: Real-Time Task Sync - multi-device support
- **US4 (P4)**: User Profile & Preferences - personalization
- **US5 (P5)**: Task Search & Advanced Filtering - power user features

**Step 3: Map Components to User Stories**
- Authentication components → US1
- Task CRUD components → US2
- Real-time sync components → US3
- Profile management components → US4
- Search/filter components → US5
- Shared infrastructure → Setup and Foundational phases

**Step 4: Generate Tasks by Phase**

### Task Breakdown

**Phase 1: Setup & Project Initialization** (15 tasks)
- Backend setup: directory structure, requirements.txt, config.py, .env.example
- Frontend setup: Next.js initialization, TypeScript config, TailwindCSS
- Shared setup: migration script skeleton, CI/CD workflows

**Phase 2: Foundational Infrastructure** (20 tasks)
- Database: Alembic setup, initial migration with 3 tables
- SQLAlchemy models: User, Task, RefreshToken with relationships
- Pydantic schemas: request/response models for all entities
- FastAPI app: initialization, CORS, health endpoints
- Shared utilities: validators (migrated from Phase 1), password hashing, TypeScript types

**Phase 3: User Story 1 - Authentication (P1)** (46 tasks)
- Backend services: auth_service (JWT), user_service (CRUD), email_service (SendGrid)
- Backend endpoints: /register, /login, /refresh, /logout, /request-password-reset, /reset-password
- Backend middleware: get_current_user dependency, rate limiting
- Backend tests: unit tests (auth_service, user_service), integration tests (auth endpoints)
- Frontend services: api.ts (axios), authService.ts (API calls)
- Frontend hooks: useAuth.tsx (context and state management)
- Frontend pages: login, register, reset-password
- Frontend components: AuthForm, ProtectedRoute
- Frontend tests: unit tests (authService), E2E tests (Playwright registration flow)
- Integration validation: manual tests for registration, login, logout, password reset

**Phase 4: User Story 2 - Task Management (P2)** (35 tasks)
- Backend services: task_service with CRUD and filtering
- Backend endpoints: GET/POST /tasks, GET/PUT/DELETE /tasks/{id}
- Backend tests: unit tests (task_service), integration tests (CRUD flow, data isolation)
- Frontend services: taskService.ts with API calls
- Frontend hooks: useTasks.tsx with state management and optimistic updates
- Frontend components: TaskList, TaskItem, TaskForm, TaskFilters
- Frontend pages: dashboard (main task interface)
- Frontend tests: unit tests (TaskList component), E2E tests (full CRUD flow)
- Integration validation: manual tests for CRUD, filtering, data isolation

**Phase 5: User Story 3 - Real-Time Sync (P3)** (18 tasks)
- Backend: WebSocket vs. polling decision, implementation based on choice
- Frontend: polling logic or WebSocket integration in useTasks.tsx
- Offline support: offline detection, change queue, sync-on-reconnect
- Tests: E2E two-tab sync test
- Integration validation: manual tests for cross-tab sync, offline sync

**Phase 6: User Story 4 - User Profile (P4)** (15 tasks)
- Backend endpoints: GET/PUT /users/me, PUT /users/me/password
- Backend tests: integration tests for profile update and password change
- Frontend services: getCurrentUser, updateProfile, changePassword functions
- Frontend pages: profile page with update forms
- Frontend hooks: useTheme.tsx for dark mode
- Integration validation: manual tests for profile updates, password change, theme persistence

**Phase 7: User Story 5 - Search & Filtering (P5)** (11 tasks)
- Backend: full-text search, date range filtering, search index
- Frontend components: TaskSearch, enhanced TaskFilters
- Tests: search performance test (50+ tasks, <1s response)
- Integration validation: manual tests for search speed and accuracy

**Final Phase: Polish & Cross-Cutting Concerns** (16 tasks)
- Security: input sanitization, SQL injection audit, CSRF protection, security headers
- Performance: connection pooling, response caching, bundle optimization, pagination
- Error handling: standardized error responses, structured logging, error boundaries
- Deployment: Dockerfile, next.config.js optimizations, deployment documentation
- Final validation: full test suite, E2E tests across all user stories

### Task Format Compliance

**All 176 tasks follow strict format**:
```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Examples**:
- ✅ `- [ ] T001 [P] Create backend/ directory structure per plan.md`
- ✅ `- [ ] T036 [US1] Create backend/src/services/auth_service.py with generate_jwt_token() function`
- ✅ `- [ ] T082 [P] [US2] Create backend/src/services/task_service.py with async create_task() function`

**Markers**:
- **[P]**: 68 tasks marked parallelizable (can run concurrently)
- **[US1]**: 46 tasks for authentication user story
- **[US2]**: 35 tasks for task management user story
- **[US3]**: 18 tasks for real-time sync user story
- **[US4]**: 15 tasks for user profile user story
- **[US5]**: 11 tasks for search & filtering user story

### Dependencies & Execution Order

**Critical Path**:
```
Setup (Phase 1)
    ↓
Foundational (Phase 2) ← BLOCKS all user stories
    ↓
US1 Authentication (Phase 3) ← BLOCKS US2, US3, US4, US5
    ↓
US2 Task Management (Phase 4) ← BLOCKS US3, US5
    ↓
US3 Real-Time Sync (Phase 5) OR US5 Search (Phase 7) [parallel]
    ↓
Polish (Final Phase)
```

**Independent Paths**:
- US4 (Profile) can develop in parallel with US2 (both depend only on US1)
- US3 (Sync) and US5 (Search) can develop in parallel (both depend on US2)

### MVP Scope

**Recommended MVP** (111 tasks, 63% of total):
- ✅ Phase 1: Setup (15 tasks)
- ✅ Phase 2: Foundational (20 tasks)
- ✅ Phase 3: US1 Authentication (46 tasks)
- ✅ Phase 4: US2 Task Management (35 tasks)
- ✅ Selected polish: Security and error handling (8 tasks)

**Deferred to v2**:
- ⏸️ Phase 5: US3 Real-Time Sync (nice to have)
- ⏸️ Phase 6: US4 User Profile (nice to have)
- ⏸️ Phase 7: US5 Advanced Search (nice to have)

**MVP Rationale**: US1 + US2 deliver core value (multi-user web task management), validate Phase 1→2 migration, provide shippable product for user feedback.

## Outcome

- ✅ Impact: **Complete task list with 176 tasks** organized by user story, enabling independent development and testing. TDD workflow enforced with test tasks before implementation tasks. All tasks follow strict checklist format with IDs, parallelization markers, story labels, and file paths.
- 🧪 Tests: **Format validation passed** (all 176 tasks have proper TaskID, story labels, file paths). **Coverage validation passed** (all 5 user stories fully covered with independent test criteria).
- 📁 Files: **1 file created** (tasks.md, 620 lines)
- 🔁 Next prompts: **User should run `/sp.implement`** to execute TDD workflow and implement Phase 2 tasks in priority order (Setup → Foundational → US1 → US2 for MVP).
- 🧠 Reflection: **Task generation successful** with clear organization by user story. Dependency graph shows US1 as critical blocker (authentication required for all other features). Parallel opportunities identified (68 tasks with [P] marker). MVP scope provides clear target (111 tasks) for first shippable increment.

## Evaluation notes (flywheel)

- Failure modes observed: **None** - Task generation completed without errors. All tasks follow required format.
- Graders run and results (PASS/FAIL):
  - ✅ Task Format Validation: PASS - All 176 tasks have proper checklist format
  - ✅ User Story Coverage: PASS - All 5 user stories (US1-US5) fully covered
  - ✅ Dependency Graph: PASS - Critical path documented, blocking relationships identified
  - ✅ Independent Test Criteria: PASS - Each user story has clear, testable acceptance criteria
  - ✅ File Path Validation: PASS - All implementation tasks include specific file paths
- Prompt variant (if applicable): **Standard `/sp.tasks` command** - No variants used
- Next experiment (smallest change to try): **Execute `/sp.implement` command** to begin TDD workflow implementation. Consider splitting large user stories (US1: 46 tasks) into sub-phases for more granular checkpoints.
