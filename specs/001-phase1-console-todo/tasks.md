# Tasks: Phase 1 - Console Todo App

**Input**: Design documents from `/specs/001-phase1-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli-commands.md

**Tests**: TDD approach - Tests are written FIRST per constitution Test-First Development principle

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create src/ directory structure (models/, services/, utils/)
- [X] T002 Create tests/ directory structure (unit/, integration/, contract/)
- [X] T003 [P] Create src/__init__.py to make src a Python package
- [X] T004 [P] Create requirements-dev.txt with pytest dependency
- [X] T005 [P] Create .gitignore file (include tasks.json, __pycache__, *.pyc, .pytest_cache)
- [X] T006 [P] Create pytest.ini configuration file in project root

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create Task model in src/models/task.py with all 7 fields from data-model.md
- [X] T008 [P] Create validation utilities in src/utils/validators.py (validate_title, validate_date, validate_priority functions)
- [X] T009 [P] Create output formatters in src/utils/formatters.py (format_task_list, format_task_single functions)
- [X] T010 Create JSON storage module in src/services/storage.py (load_tasks, save_tasks with atomic writes)
- [X] T011 Create task service in src/services/task_service.py (get_next_id, create_task, get_all_tasks functions)
- [X] T012 Create main CLI entry point in src/todo_cli.py with argparse setup and subparsers

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can quickly capture tasks and see all pending work at a glance

**Independent Test**: Run CLI, add one or more tasks via command, then list all tasks to verify they appear with correct details

### Tests for User Story 1 (TDD - Write these tests FIRST) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US1] Write contract test for "add minimal task" in tests/contract/test_cli_interface.py
- [X] T014 [P] [US1] Write contract test for "add full task with all options" in tests/contract/test_cli_interface.py
- [X] T015 [P] [US1] Write contract test for "add task with empty title error" in tests/contract/test_cli_interface.py
- [X] T016 [P] [US1] Write contract test for "add task with invalid date error" in tests/contract/test_cli_interface.py
- [X] T017 [P] [US1] Write contract test for "list all tasks" in tests/contract/test_cli_interface.py
- [X] T018 [P] [US1] Write contract test for "list empty tasks" in tests/contract/test_cli_interface.py
- [X] T019 [P] [US1] Write unit test for Task model creation in tests/unit/test_task_model.py
- [X] T020 [P] [US1] Write unit test for validate_title function in tests/unit/test_validators.py
- [X] T021 [P] [US1] Write unit test for validate_date function in tests/unit/test_validators.py
- [X] T022 [P] [US1] Write unit test for validate_priority function in tests/unit/test_validators.py
- [X] T023 [P] [US1] Write unit test for get_next_id function in tests/unit/test_task_service.py
- [X] T024 [P] [US1] Write unit test for create_task function in tests/unit/test_task_service.py
- [X] T025 [P] [US1] Write integration test for storage load/save in tests/integration/test_storage.py
- [X] T026 [P] [US1] Write integration test for add+list workflow in tests/integration/test_cli_workflows.py

### Implementation for User Story 1

- [X] T027 [US1] Implement add_task function in src/services/task_service.py (validate input, assign ID, create task dict)
- [X] T028 [US1] Implement list_tasks function in src/services/task_service.py (load tasks, apply filters, return list)
- [X] T029 [US1] Implement add command handler in src/todo_cli.py (parse args, call add_task, save, print success)
- [X] T030 [US1] Implement list command handler in src/todo_cli.py (parse args, call list_tasks, format output)
- [X] T031 [US1] Verify all US1 tests pass - run pytest tests/contract/test_cli_interface.py::test_add* and ::test_list*

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can mark tasks as complete to track progress and feel accomplished

**Independent Test**: Add a task, mark it complete by ID, then list tasks to verify status changed to "completed"

### Tests for User Story 2 (TDD - Write these tests FIRST) ⚠️

- [ ] T032 [P] [US2] Write contract test for "complete task success" in tests/contract/test_cli_interface.py
- [ ] T033 [P] [US2] Write contract test for "complete nonexistent task error" in tests/contract/test_cli_interface.py
- [ ] T034 [P] [US2] Write unit test for complete_task function in tests/unit/test_task_service.py
- [ ] T035 [P] [US2] Write integration test for add→complete→verify workflow in tests/integration/test_cli_workflows.py

### Implementation for User Story 2

- [ ] T036 [US2] Implement complete_task function in src/services/task_service.py (find task by ID, update status to "completed", save)
- [ ] T037 [US2] Implement complete command handler in src/todo_cli.py (parse task_id arg, call complete_task, print success/error)
- [ ] T038 [US2] Add visual distinction for completed tasks in src/utils/formatters.py (e.g., checkmark, color)
- [ ] T039 [US2] Verify all US2 tests pass - run pytest tests/contract/test_cli_interface.py::test_complete*

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can modify task details when priorities change or information needs correction

**Independent Test**: Create a task, update its title or description via command, then list to verify changes persisted

### Tests for User Story 3 (TDD - Write these tests FIRST) ⚠️

- [ ] T040 [P] [US3] Write contract test for "update task title" in tests/contract/test_cli_interface.py
- [ ] T041 [P] [US3] Write contract test for "update task no fields error" in tests/contract/test_cli_interface.py
- [ ] T042 [P] [US3] Write contract test for "update nonexistent task error" in tests/contract/test_cli_interface.py
- [ ] T043 [P] [US3] Write unit test for update_task function in tests/unit/test_task_service.py

### Implementation for User Story 3

- [ ] T044 [US3] Implement update_task function in src/services/task_service.py (find task, validate new values, update fields, save)
- [ ] T045 [US3] Implement update command handler in src/todo_cli.py (parse task_id and optional fields, call update_task, print success)
- [ ] T046 [US3] Verify all US3 tests pass - run pytest tests/contract/test_cli_interface.py::test_update*

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can remove tasks that are no longer relevant or were added by mistake

**Independent Test**: Create a task, delete it by ID, then list tasks to verify it no longer appears

### Tests for User Story 4 (TDD - Write these tests FIRST) ⚠️

- [ ] T047 [P] [US4] Write contract test for "delete task with confirm" in tests/contract/test_cli_interface.py
- [ ] T048 [P] [US4] Write contract test for "delete nonexistent task error" in tests/contract/test_cli_interface.py
- [ ] T049 [P] [US4] Write contract test for "delete task cancelled" in tests/contract/test_cli_interface.py (using monkeypatch)
- [ ] T050 [P] [US4] Write unit test for delete_task function in tests/unit/test_task_service.py

### Implementation for User Story 4

- [ ] T051 [US4] Implement delete_task function in src/services/task_service.py (find task, remove from list, save)
- [ ] T052 [US4] Implement delete command handler in src/todo_cli.py (parse task_id, confirm prompt unless --confirm flag, call delete_task)
- [ ] T053 [US4] Verify all US4 tests pass - run pytest tests/contract/test_cli_interface.py::test_delete*

**Checkpoint**: User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Filter Tasks by Status (Priority: P5)

**Goal**: Users can view only pending or only completed tasks to focus on active work

**Independent Test**: Create a mix of pending and completed tasks, then list with status filter to verify only matching tasks appear

### Tests for User Story 5 (TDD - Write these tests FIRST) ⚠️

- [ ] T054 [P] [US5] Write contract test for "list filter pending" in tests/contract/test_cli_interface.py
- [ ] T055 [P] [US5] Write contract test for "list filter completed" in tests/contract/test_cli_interface.py
- [ ] T056 [P] [US5] Write contract test for "list filter by priority" in tests/contract/test_cli_interface.py
- [ ] T057 [P] [US5] Write unit test for filter_tasks function in tests/unit/test_task_service.py

### Implementation for User Story 5

- [ ] T058 [US5] Implement filter_tasks function in src/services/task_service.py (filter by status, priority)
- [ ] T059 [US5] Update list command handler in src/todo_cli.py to support --status and --priority filters
- [ ] T060 [US5] Add --sort-by option to list command in src/todo_cli.py (sort by id, title, due_date, priority, created_at)
- [ ] T061 [US5] Verify all US5 tests pass - run pytest tests/contract/test_cli_interface.py::test_list_filter*

**Checkpoint**: All user stories (1-5) should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T062 [P] Add comprehensive error handling for FileNotFoundError in src/services/storage.py (first run scenario)
- [ ] T063 [P] Add error handling for JSONDecodeError in src/services/storage.py (corrupted file scenario)
- [ ] T064 [P] Implement atomic file writes in src/services/storage.py (temp file + rename pattern)
- [ ] T065 [P] Add input validation for title max length (200 chars) in src/utils/validators.py
- [ ] T066 [P] Add input validation for description max length (1000 chars) in src/utils/validators.py
- [ ] T067 [P] Write unit tests for all edge cases in tests/unit/test_validators.py (empty title, long title, invalid dates, special characters)
- [ ] T068 [P] Write integration test for corrupted JSON file recovery in tests/integration/test_storage.py
- [ ] T069 [P] Write integration test for first-run scenario (no tasks.json) in tests/integration/test_storage.py
- [ ] T070 [P] Add help text and examples to all argparse commands in src/todo_cli.py
- [ ] T071 [P] Write unit tests for output formatting in tests/unit/test_formatters.py (table format, empty state, single task)
- [ ] T072 Run full test suite and ensure 100% pass rate - pytest tests/ -v
- [ ] T073 Test quickstart.md examples manually to validate user guide accuracy
- [ ] T074 Create README.md with installation and basic usage instructions
- [ ] T075 Run constitution compliance check - verify TDD workflow followed, no external dependencies, stdlib only

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Reuses US1 components (task creation) but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Reuses US1 components (task creation) but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Reuses US1 components (task creation) but independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Enhances US1 list functionality but independently testable

### Within Each User Story

- Tests (TDD) MUST be written and FAIL before implementation
- All tests for a story can be written in parallel (marked with [P])
- Implementation tasks follow test completion
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup phase (T001-T006)**: All tasks marked [P] can run in parallel
- **Foundational phase (T007-T012)**: Tasks T008, T009 can run in parallel with others
- **User Story tests**: Within each story, all test tasks marked [P] can run in parallel
- **Once Foundational complete**: All user stories can be developed in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (TDD - write tests first):
Task: "Write contract test for add minimal task in tests/contract/test_cli_interface.py"
Task: "Write contract test for add full task in tests/contract/test_cli_interface.py"
Task: "Write contract test for add empty title error in tests/contract/test_cli_interface.py"
Task: "Write contract test for add invalid date error in tests/contract/test_cli_interface.py"
Task: "Write contract test for list all tasks in tests/contract/test_cli_interface.py"
Task: "Write contract test for list empty tasks in tests/contract/test_cli_interface.py"
Task: "Write unit test for Task model in tests/unit/test_task_model.py"
Task: "Write unit test for validators in tests/unit/test_validators.py"
Task: "Write unit test for task service in tests/unit/test_task_service.py"
Task: "Write integration test for storage in tests/integration/test_storage.py"
Task: "Write integration test for workflow in tests/integration/test_cli_workflows.py"

# After all tests written and FAILING, implement in sequence:
Task: "Implement add_task function in src/services/task_service.py"
Task: "Implement list_tasks function in src/services/task_service.py"
Task: "Implement add command handler in src/todo_cli.py"
Task: "Implement list command handler in src/todo_cli.py"
Task: "Verify all US1 tests pass"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T012) - CRITICAL blocker
3. Complete Phase 3: User Story 1 (T013-T031)
   - Write all tests FIRST (T013-T026)
   - Verify tests FAIL
   - Implement functionality (T027-T030)
   - Verify tests PASS (T031)
4. **STOP and VALIDATE**: Test User Story 1 independently using quickstart.md examples
5. Ready for Phase 2 migration planning or continue with P2-P5 stories

### Incremental Delivery

1. Complete Setup + Foundational (T001-T012) → Foundation ready
2. Add User Story 1 (T013-T031) → Test independently → MVP ready! ✅
3. Add User Story 2 (T032-T039) → Test independently → Progress tracking available
4. Add User Story 3 (T040-T046) → Test independently → Task editing available
5. Add User Story 4 (T047-T053) → Test independently → Task deletion available
6. Add User Story 5 (T054-T061) → Test independently → Filtering complete
7. Polish (T062-T075) → Production-ready

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T012)
2. Once Foundational is done:
   - Developer A: User Story 1 (T013-T031)
   - Developer B: User Story 2 (T032-T039) - can start in parallel
   - Developer C: User Story 3 (T040-T046) - can start in parallel
3. Stories complete and integrate independently
4. Team collaborates on Polish phase (T062-T075)

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label (US1-US5) maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **TDD CRITICAL**: Tests written FIRST (T013-T026 for US1, etc.), verify FAIL, then implement
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitution compliance: Python 3.11+, stdlib only, pytest for testing, TDD workflow
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Count Summary

- **Phase 1 (Setup)**: 6 tasks
- **Phase 2 (Foundational)**: 6 tasks (BLOCKS all stories)
- **Phase 3 (US1 - Add/View)**: 19 tasks (14 tests + 5 implementation)
- **Phase 4 (US2 - Complete)**: 8 tasks (4 tests + 4 implementation)
- **Phase 5 (US3 - Update)**: 7 tasks (4 tests + 3 implementation)
- **Phase 6 (US4 - Delete)**: 7 tasks (4 tests + 3 implementation)
- **Phase 7 (US5 - Filter)**: 8 tasks (4 tests + 4 implementation)
- **Phase 8 (Polish)**: 14 tasks

**Total: 75 tasks**

**Test tasks: 30 (40% - strong TDD compliance)**
**Implementation tasks: 45**

**MVP Scope (Phase 1-3)**: 31 tasks (Setup + Foundational + US1)
**Full Phase 1**: All 75 tasks
