# Data Model: Todo Backend API & Database Layer

## Overview
This document defines the database schema and entity relationships for the Todo Full-Stack Web Application backend API & Database Layer, ensuring proper user isolation and data integrity.

## Entity: User
**Description**: Represents an authenticated user in the system with unique identifier and email

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `email`: String (max_length=255, unique, required)
- `created_at`: DateTime (auto-generated timestamp)
- `updated_at`: DateTime (auto-generated timestamp, updated on change)

**Validation rules**:
- Email must be valid email format
- Email must be unique across all users
- ID must be UUID format

**Relationships**:
- One-to-Many with Task (via user_id foreign key)

## Entity: Task
**Description**: Represents a task item owned by a specific user

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `user_id`: UUID (Foreign Key to User.id, required)
- `title`: String (max_length=255, required)
- `description`: Text (optional, nullable)
- `completed`: Boolean (default: False)
- `created_at`: DateTime (auto-generated timestamp)
- `updated_at`: DateTime (auto-generated timestamp, updated on change)

**Validation rules**:
- Title must be between 1 and 255 characters
- User_id must reference an existing User.id
- Completed field defaults to False if not provided

**Relationships**:
- Many-to-One with User (via user_id foreign key)

## Database Constraints
- Foreign key constraint: tasks.user_id references users.id
- Cascade delete: When a user is deleted, their tasks are also deleted
- Index on user_id in tasks table for efficient user-scoped queries
- Unique constraint on email in users table
- Primary key constraints on id fields

## State Transitions
- Task.completed can transition from False to True (completed) or True to False (uncompleted) via PATCH /complete endpoint

## Security Considerations
- All queries must be scoped by user_id to enforce data isolation
- Direct access to tasks must include user_id filter to prevent unauthorized access
- Foreign key constraints ensure referential integrity