<!--
SYNC IMPACT REPORT:
- Version change: N/A → 1.0.0 (initial version)
- Added sections: All principles and sections from user input
- Templates requiring updates: N/A
- Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-driven development
Every implementation decision must trace back to a written specification.

### Security-first design
Authentication, authorization, and data isolation are mandatory and non-negotiable.

### Separation of concerns
Frontend, backend, authentication, and database responsibilities must remain clearly separated.

### Stateless architecture
Backend services must rely on JWT-based authentication, not shared sessions.

### Reproducibility
All steps, prompts, and iterations must be traceable and repeatable.

## Key Standards

- All backend APIs must be RESTful and follow HTTP standards
- Every API request must be authenticated using a valid JWT
- Task ownership must be enforced at the database query level
- Frontend must never access or infer data belonging to other users
- Authentication must be handled exclusively via Better Auth on the frontend
- Backend must verify JWTs independently using a shared secret
- Database schema changes must be handled through migrations
- Environment secrets must never be hardcoded

## Constraints

- No manual coding: all code must be generated via the Agentic Dev Stack workflow
- Technology stack is fixed:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Auth: Better Auth + JWT
- All endpoints must require authentication
- API behavior must match the defined endpoint contract exactly
- Each user must only see and modify their own tasks

## Security Requirements

- JWT tokens must be validated for:
  - Signature
  - Expiration
  - User identity
- Requests without valid JWTs must return `401 Unauthorized`
- User ID in the JWT must match the user scope of the request
- No shared database sessions between frontend and backend
- Tokens must be passed via `Authorization: Bearer <token>` header

## Quality Standards

- Clear error handling with correct HTTP status codes
- Consistent API responses following established patterns
- Proper input validation on both frontend and backend
- Comprehensive error logging for debugging and monitoring
- Performance optimization for user experience
- Responsive design for cross-device compatibility

## Development Workflow

- Specifications must be written before any implementation begins
- Plans must be generated and approved before task breakdown
- Tasks must be broken down with acceptance criteria before implementation
- All changes must be tracked through the Agentic Dev Stack
- Testing must be integrated throughout the development process
- Documentation must be maintained alongside code changes

## Governance

This constitution governs all development activities for the Todo Full-Stack Web Application. All team members must adhere to these principles and standards. Any deviation from these principles must be documented and approved through the formal amendment process.

Amendments to this constitution require:
- Written justification for the proposed change
- Team review and approval
- Update to all dependent artifacts and documentation
- Clear migration plan for existing codebase if applicable

**Version**: 1.0.0 | **Ratified**: 2026-01-18 | **Last Amended**: 2026-01-18
