---
description: "Task list for Todo Backend API & Database Layer implementation"
---

# Tasks: Todo Backend API & Database Layer

**Input**: Design documents from `/specs/001-backend-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in backend/
- [X] T002 Initialize Python project with FastAPI, SQLModel, Pydantic dependencies in backend/requirements.txt
- [X] T003 [P] Configure linting and formatting tools (black, flake8, mypy) in backend/pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup database schema and migrations framework with Alembic in backend/alembic/
- [X] T005 [P] Implement JWT authentication framework in backend/src/utils/jwt_utils.py
- [X] T006 [P] Setup API routing and middleware structure in backend/src/api/
- [X] T007 Create base models/entities that all stories depend on in backend/src/models/base.py
- [X] T008 Configure error handling and logging infrastructure in backend/src/utils/security.py
- [X] T009 Setup environment configuration management in backend/src/config/settings.py
- [X] T010 Create User and Task models in backend/src/models/user.py and backend/src/models/task.py
- [X] T011 Create User and Task schemas in backend/src/schemas/user.py and backend/src/schemas/task.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Secure Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable registered users to manage their personal tasks through a secure API that ensures their data remains private from other users

**Independent Test**: Can be fully tested by authenticating as a user, creating tasks, retrieving them, updating them, and deleting them while ensuring other users cannot access these tasks

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T012 [P] [US1] Contract test for GET /api/{user_id}/tasks in backend/tests/test_tasks.py
- [X] T013 [P] [US1] Contract test for POST /api/{user_id}/tasks in backend/tests/test_tasks.py
- [X] T014 [P] [US1] Contract test for GET /api/{user_id}/tasks/{id} in backend/tests/test_tasks.py
- [X] T015 [P] [US1] Contract test for PUT /api/{user_id}/tasks/{id} in backend/tests/test_tasks.py
- [X] T016 [P] [US1] Contract test for DELETE /api/{user_id}/tasks/{id} in backend/tests/test_tasks.py

### Implementation for User Story 1

- [X] T017 [P] [US1] Create TaskService in backend/src/services/task_service.py (handles business logic)
- [X] T018 [US1] Create authentication dependency in backend/src/api/deps.py
- [X] T019 [US1] Implement GET /api/{user_id}/tasks endpoint in backend/src/api/v1/endpoints/tasks.py
- [X] T020 [US1] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/v1/endpoints/tasks.py
- [X] T021 [US1] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/v1/endpoints/tasks.py
- [X] T022 [US1] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/v1/endpoints/tasks.py
- [X] T023 [US1] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/v1/endpoints/tasks.py
- [X] T024 [US1] Add validation and error handling to task endpoints
- [X] T025 [US1] Add logging for user story 1 operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Completion Toggle (Priority: P2)

**Goal**: Allow users to mark their tasks as completed or incomplete through a dedicated endpoint

**Independent Test**: Can be tested by authenticating as a user, toggling the completion status of a task, and verifying the status was updated correctly

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T026 [P] [US2] Contract test for PATCH /api/{user_id}/tasks/{id}/complete in backend/tests/test_tasks.py

### Implementation for User Story 2

- [X] T027 [US2] Extend TaskService with completion toggle functionality in backend/src/services/task_service.py
- [X] T028 [US2] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/v1/endpoints/tasks.py
- [X] T029 [US2] Add validation and error handling for completion toggle
- [X] T030 [US2] Add logging for user story 2 operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure Access Control (Priority: P3)

**Goal**: Prevent unauthorized access and ensure users can only interact with their own data

**Independent Test**: Can be tested by attempting to access another user's tasks with a valid JWT for a different user, which should be rejected

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T031 [P] [US3] Integration test for user isolation in backend/tests/integration/test_task_isolation.py

### Implementation for User Story 3

- [X] T032 [US3] Enhance authentication dependency to verify JWT user ID matches URL user ID in backend/src/api/deps.py
- [X] T033 [US3] Add user ID verification to all task endpoints in backend/src/api/v1/endpoints/tasks.py
- [X] T034 [US3] Implement database-level user scoping for all queries in backend/src/services/task_service.py
- [X] T035 [US3] Add comprehensive error handling for access control violations

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T036 [P] Documentation updates in backend/README.md
- [X] T037 Code cleanup and refactoring
- [ ] T038 Performance optimization across all stories
- [X] T039 [P] Additional unit tests (if requested) in backend/tests/
- [X] T040 Security hardening
- [ ] T041 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for GET /api/{user_id}/tasks in backend/tests/test_tasks.py"
Task: "Contract test for POST /api/{user_id}/tasks in backend/tests/test_tasks.py"
Task: "Contract test for GET /api/{user_id}/tasks/{id} in backend/tests/test_tasks.py"
Task: "Contract test for PUT /api/{user_id}/tasks/{id} in backend/tests/test_tasks.py"
Task: "Contract test for DELETE /api/{user_id}/tasks/{id} in backend/tests/test_tasks.py"

# Launch all models for User Story 1 together:
Task: "Create TaskService in backend/src/services/task_service.py"
Task: "Create authentication dependency in backend/src/api/deps.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence