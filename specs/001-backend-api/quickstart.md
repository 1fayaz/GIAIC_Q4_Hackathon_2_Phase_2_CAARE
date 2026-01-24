# Quickstart Guide: Todo Backend API & Database Layer

## Overview
This guide provides instructions for setting up, running, and testing the Todo Full-Stack Web Application backend API & Database Layer.

## Prerequisites
- Python 3.11+
- pip package manager
- Neon Serverless PostgreSQL database instance
- Better Auth configured to generate JWT tokens

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd backend
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the backend root directory:
```bash
DATABASE_URL=postgresql://username:password@neon-host.region.neon.tech/dbname
JWT_SECRET_KEY=your-super-secret-jwt-signing-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

### 5. Initialize Database
```bash
alembic upgrade head
```

### 6. Run the Application
```bash
uvicorn src.main:app --reload --port 8000
```

## API Endpoints

### Task Management
- `GET /api/{user_id}/tasks` - List all tasks for the user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

### Headers Required
All endpoints require:
- `Authorization: Bearer <valid-jwt-token>`
- JWT must have user_id claim matching the user_id in URL

## Testing the API

### Authentication Test
```bash
curl -X GET http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer <valid-jwt>"
```

### Create Task Test
```bash
curl -X POST http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer <valid-jwt>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Test description"}'
```

### Expected Responses
- Successful operations return 200/201 status codes
- Invalid JWT returns 401 Unauthorized
- User ID mismatch returns 403 Forbidden
- Non-existent resources return 404 Not Found

## Running Tests
```bash
pytest
```

## Troubleshooting
- If database connection fails, verify DATABASE_URL is correct
- If JWT validation fails, check JWT_SECRET_KEY matches the one used by Better Auth
- If user isolation isn't working, ensure all queries are scoped by user_id