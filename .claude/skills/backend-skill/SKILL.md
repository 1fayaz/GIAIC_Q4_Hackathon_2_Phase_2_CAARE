---
name: backend-skill
description: Generate backend routes, handle requests and responses, and connect securely to databases.
---

# Backend Skill – Routes, Requests & Database Integration

## Instructions

1. **Route Generation**
   - Define clear and RESTful API routes
   - Use proper HTTP methods (GET, POST, PUT, DELETE)
   - Group routes by resource or domain
   - Apply versioning where necessary
   - Keep route naming consistent and predictable

2. **Request Handling**
   - Validate incoming requests strictly
   - Parse and sanitize input data
   - Handle query parameters, path params, and request bodies correctly
   - Apply authentication and authorization checks
   - Use middleware/dependencies for cross-cutting concerns

3. **Response Handling**
   - Return consistent response formats
   - Use appropriate HTTP status codes
   - Handle errors gracefully and explicitly
   - Avoid leaking internal implementation details
   - Include pagination and metadata when applicable

4. **Database Connection**
   - Establish and manage database connections safely
   - Use ORMs or query builders appropriately
   - Execute queries within transactions when required
   - Prevent SQL/NoSQL injection
   - Handle connection pooling and lifecycle management

## Best Practices
- Keep business logic separate from routing logic
- Validate data at both API and database layers
- Use async/non-blocking I/O where possible
- Log requests and errors without sensitive data
- Centralize error handling
- Write unit and integration tests for routes

## Example Structure
```ts
// Route
GET /users

// Handler flow
- Validate request
- Fetch data from DB
- Transform result
- Return response

// Example response
{
  "data": [],
  "meta": { "count": 0 }
}
