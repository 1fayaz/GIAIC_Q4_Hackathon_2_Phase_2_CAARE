# Data Model: Frontend UI, Auth & Interactive Effects

**Feature**: 003-frontend-auth-integration
**Date**: 2026-01-22
**Author**: Claude Code

## Frontend Data Structures

### User Entity
- **Fields**:
  - `id`: string (unique identifier)
  - `email`: string (user email address)
  - `is_active`: boolean (account status)
  - `is_verified`: boolean (email verification status)
  - `created_at`: string (ISO date format)
  - `updated_at`: string (ISO date format)

- **Validation**:
  - Email must be valid format
  - ID must be unique
  - Required fields: id, email

### Task Entity
- **Fields**:
  - `id`: string (unique identifier)
  - `title`: string (task title)
  - `description`: string | null (task description)
  - `completed`: boolean (completion status)
  - `user_id`: string (foreign key to user)
  - `created_at`: string (ISO date format)
  - `updated_at`: string (ISO date format)

- **Validation**:
  - Title is required
  - User_id must match authenticated user
  - Completed defaults to false

### API Response Entity
- **Fields**:
  - `success`: boolean (request success status)
  - `data`: any (response data payload)
  - `error`: string | null (error message if any)
  - `status`: number (HTTP status code)

### Authentication Token
- **Fields**:
  - `access_token`: string (JWT token)
  - `token_type`: string (typically "Bearer")
  - `expires_in`: number (seconds until expiration)
  - `user_id`: string (associated user ID)

## State Management Objects

### Authentication State
- **Fields**:
  - `user`: User | null (authenticated user data)
  - `isAuthenticated`: boolean (auth status)
  - `isLoading`: boolean (loading state during auth check)
  - `error`: string | null (auth error message)

### Task State
- **Fields**:
  - `tasks`: Task[] (list of user's tasks)
  - `loading`: boolean (loading state)
  - `error`: string | null (error message)
  - `currentTaskId`: string | null (currently viewed/edited task)

### UI State
- **Fields**:
  - `activeTab`: string (currently selected navigation tab)
  - `glowPosition`: {x: number, y: number} (pointer position for glow effects)
  - `isTouchDevice`: boolean (touch device detection)

## API Contract Types

### Request Types
- `UserLoginRequest`: {email: string, password: string}
- `UserRegisterRequest`: {email: string, password: string}
- `TaskCreateRequest`: {title: string, description?: string, user_id: string}
- `TaskUpdateRequest`: {title?: string, description?: string, completed?: boolean}

### Response Types
- `UserLoginResponse`: {access_token: string, token_type: string, user_id: string, email: string}
- `TaskResponse`: Task entity with additional backend fields
- `ApiErrorResponse`: {error: string, status: number}