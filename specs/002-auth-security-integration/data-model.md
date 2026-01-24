# Data Model: Authentication & Security Integration

## Overview
This document defines the data models required for implementing authentication and security using Better Auth (frontend) and JWT-based verification (backend) in the Todo Full-Stack Web Application.

## Entities

### User
**Description**: Represents an authenticated user in the system

**Fields**:
- `id` (String/UUID): Unique identifier for the user
- `email` (String): User's email address, used for authentication
- `name` (String): User's display name
- `password_hash` (String): Hashed password for the user account
- `created_at` (DateTime): Timestamp when the user account was created
- `updated_at` (DateTime): Timestamp when the user account was last updated
- `is_active` (Boolean): Flag indicating if the user account is active

**Relationships**:
- One-to-many with Todo items (user owns multiple todos)
- One-to-many with Session records (user has multiple sessions)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Name must be between 1-100 characters
- Password must meet security requirements (minimum length, complexity)

### JWT Token
**Description**: Represents a JSON Web Token for authentication

**Fields**:
- `token` (String): The JWT token string
- `user_id` (String/UUID): Reference to the associated user
- `expires_at` (DateTime): Expiration timestamp for the token
- `issued_at` (DateTime): Creation timestamp for the token
- `type` (String): Type of token (access, refresh)
- `revoked` (Boolean): Flag indicating if the token has been revoked

**Relationships**:
- Many-to-one with User (token belongs to one user)

**Validation Rules**:
- Token must be a valid JWT format
- Expires_at must be in the future
- Type must be either 'access' or 'refresh'

### Authenticated Request
**Description**: Represents an API request with authentication context

**Fields**:
- `request_id` (String/UUID): Unique identifier for the request
- `user_id` (String/UUID): User ID extracted from JWT
- `endpoint` (String): The API endpoint being accessed
- `method` (String): HTTP method (GET, POST, PUT, DELETE)
- `timestamp` (DateTime): When the request was made
- `status` (String): Authentication status (valid, invalid, expired)

**Relationships**:
- Many-to-one with User (request is made by one user)

**Validation Rules**:
- User ID must match the authenticated user
- Endpoint must be accessible to the authenticated user
- Request must have a valid JWT token

## State Transitions

### User Account States
- **Inactive**: New user account awaiting activation
- **Active**: Verified and active user account
- **Suspended**: Temporarily suspended account
- **Deactivated**: Permanently deactivated account

### JWT Token States
- **Valid**: Token exists and has not expired
- **Expired**: Token has passed its expiration time
- **Revoked**: Token was manually invalidated before expiration
- **Invalid**: Token signature verification failed

## Security Constraints

### User Data Protection
- Passwords must be hashed using bcrypt or similar algorithm
- Personal information must be encrypted at rest
- User IDs must be globally unique
- Email addresses must be verified before full account activation

### JWT Security
- JWTs must include expiration time
- JWT signatures must be verified using shared secret
- JWT claims must match expected user identity
- Refresh tokens must be stored securely and rotated periodically

## API Contract Implications

### Authentication Endpoints
- `/auth/signup`: Creates new user account and returns JWT
- `/auth/signin`: Validates credentials and returns JWT
- `/auth/refresh`: Exchanges refresh token for new access token
- `/auth/logout`: Revokes current JWT token

### User-Scoped Operations
- All user-specific data operations must validate JWT user ID matches request context
- User endpoints must enforce ownership of requested resources
- Cross-user data access must be prevented through authorization checks