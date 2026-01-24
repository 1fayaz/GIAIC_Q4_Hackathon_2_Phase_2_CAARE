# Todo Backend API

This is the backend API for the Todo Full-Stack Web Application, built with FastAPI and secured with JWT authentication.

## Features

- Secure task management with JWT-based authentication
- User isolation - each user can only access their own tasks
- RESTful API endpoints for task operations
- SQLModel ORM for database operations
- Neon Serverless PostgreSQL database

## Tech Stack

- Python 3.11
- FastAPI
- SQLModel
- Pydantic
- Uvicorn
- python-jose for JWT handling
- passlib for password hashing
- Alembic for database migrations

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@host:port/database
   JWT_SECRET_KEY=your-super-secret-jwt-signing-key-here
   ```

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the development server:
   ```bash
   uvicorn src.main:app --reload
   ```

## API Endpoints

The API provides the following endpoints for task management:

- `GET /api/{user_id}/tasks` - List all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

All endpoints require a valid JWT token in the Authorization header.

## Security

- All endpoints require JWT authentication
- User ID in the URL must match the user ID in the JWT token
- Users can only access their own tasks
- Passwords are securely hashed using bcrypt
- JWT tokens are signed with a secret key and have expiration times

## Development

- Use black for code formatting
- Use flake8 for linting
- Write tests with pytest
- Follow FastAPI best practices