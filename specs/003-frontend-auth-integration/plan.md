# Implementation Plan: Frontend UI, Auth & Interactive Effects

**Feature**: 003-frontend-auth-integration
**Date**: 2026-01-22
**Author**: Claude Code

---

## Technical Context

This plan implements the frontend application for the Todo Full-Stack Web Application, featuring Next.js 16+ with App Router, Better Auth integration, and interactive glow effects. The system will provide a responsive, authenticated UI that securely communicates with the FastAPI backend using JWT-based authentication.

The frontend will include:
- Authentication flows (sign-up/sign-in) using Better Auth
- Secure JWT token handling and API communication
- Task management UI with CRUD operations
- Interactive glow effects for enhanced user experience
- Responsive design across desktop and mobile

Technologies involved:
- Next.js 16+ with App Router
- TypeScript
- Better Auth for authentication
- Shadcn UI for base components
- Tailwind CSS for styling and glow effects
- FastAPI backend integration

## Architecture Overview

- **App Router**: Public routes (auth) and protected routes (tasks)
- **Auth Layer**: Better Auth provider with JWT session handling
- **API Client**: Centralized fetch wrapper with automatic Authorization header injection
- **UI Layer**: Shadcn UI components with custom glow-enhanced components
- **Interaction Layer**: Pointer-tracking logic with CSS variable-driven glow effects

## Constitution Check

All implementation must comply with the project constitution regarding:
- Security-first approach (secure JWT handling)
- Responsive design principles
- Clean separation of concerns
- Accessibility standards
- Performance optimization

## Gates

### Gate 1: Security Requirements
- [ ] JWT tokens stored securely in frontend
- [ ] All API requests include proper Authorization headers
- [ ] Authentication state properly managed
- [ ] No hardcoded secrets in frontend code

### Gate 2: Architecture Compliance
- [ ] Proper separation between App Router, Auth, API Client, UI, and Interaction layers
- [ ] Shadcn UI components properly integrated
- [ ] Better Auth integration follows best practices
- [ ] Responsive design principles implemented

### Gate 3: Interactive Effects Implementation
- [ ] Glow effects work without breaking layout
- [ ] Effects are disabled on touch devices if needed
- [ ] Pointer tracking performs smoothly
- [ ] CSS variables properly drive glow behavior

### Gate 4: Implementation Feasibility
- [ ] Technology stack alignment verified
- [ ] Integration points clearly defined
- [ ] Dependencies properly documented
- [ ] Testing approach outlined

---

## Phase 0: Outline & Research

### Research Tasks to be Completed

#### 1. Next.js App Router Best Practices
- **To Research**: Optimal folder structure for auth vs protected routes
- **Focus**: Layout nesting, loading states, error boundaries

#### 2. Better Auth Integration Patterns
- **To Research**: JWT token handling with Next.js App Router
- **Focus**: Session management, token refresh, error handling

#### 3. Glow Effect Implementation Approaches
- **To Research**: CSS variable-driven glow effects without canvas
- **Focus**: Pointer tracking performance, smooth transitions, touch device compatibility

#### 4. Shadcn UI Integration
- **To Research**: Proper setup with Next.js and Tailwind CSS
- **Focus**: Component customization, theming, accessibility

#### 5. API Client Architecture
- **To Research**: Centralized fetch wrapper with JWT injection
- **Focus**: Error handling, loading states, caching strategies

---

## Phase 1: Design & Contracts

### Component Structure

#### App Router Structure
```
app/
├── layout.tsx                 # Root layout (theme + font)
├── page.tsx                   # Landing page
├── sign-in/                   # Public auth routes
│   ├── page.tsx
│   └── layout.tsx
├── sign-up/
│   ├── page.tsx
│   └── layout.tsx
├── dashboard/                 # Protected routes
│   ├── layout.tsx             # App layout (navigation + content)
│   ├── page.tsx               # Dashboard home
│   └── tasks/
│       ├── page.tsx
│       └── [id]/
│           └── page.tsx
└── globals.css
```

#### Auth Components
- `SignInForm`: Shadcn Form with Better Auth integration
- `SignUpForm`: Registration form with validation
- `AuthGuard`: Route protection component
- `AuthProvider`: Better Auth context provider

#### Task Components
- `TaskCard`: Glow-enabled card component
- `TaskList`: Container for multiple task cards
- `TaskForm`: Create/update form component
- `TaskActions`: Edit, delete, complete action buttons

#### UI Effects Components
- `GlowCard`: Wrapper for glow-enhanced cards
- `GlowLayer`: Pointer tracking layer
- `GlowTabs`: Navigation with glow effects

### API Contracts

#### Authentication Endpoints
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/token` - Token refresh
- `GET /api/v1/auth/me` - Current user profile

#### Task Management Endpoints
- `GET /api/v1/{user_id}/tasks` - List user tasks
- `POST /api/v1/{user_id}/tasks` - Create new task
- `GET /api/v1/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/v1/{user_id}/tasks/{id}` - Update task
- `DELETE /api/v1/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/v1/{user_id}/tasks/{id}/complete` - Toggle completion

### Data Models

#### Frontend Data Structures
- `User`: User profile information from authentication
- `Task`: Task entity with title, description, completion status, timestamps
- `ApiResponse`: Standardized API response format

---

## Phase 2: Implementation Tasks

### Task 1: Project Setup & Dependencies
- [ ] Initialize Next.js project with TypeScript
- [ ] Install and configure Shadcn UI
- [ ] Set up Tailwind CSS for styling
- [ ] Install Better Auth dependencies
- [ ] Configure environment variables

### Task 2: App Router Structure
- [ ] Create root layout with theme and font
- [ ] Implement auth layout for minimal UI
- [ ] Create app layout with navigation and content
- [ ] Set up route protection with AuthGuard

### Task 3: Authentication Implementation
- [ ] Set up Better Auth provider
- [ ] Create sign-in form with validation
- [ ] Create sign-up form with validation
- [ ] Implement JWT token storage and retrieval
- [ ] Add route protection logic

### Task 4: API Client Layer
- [ ] Create centralized fetch wrapper
- [ ] Implement automatic Authorization header injection
- [ ] Add error handling and loading states
- [ ] Create API service functions for all endpoints

### Task 5: Task Management UI
- [ ] Create TaskCard component with glow effects
- [ ] Implement TaskList container
- [ ] Build TaskForm for create/update operations
- [ ] Develop TaskActions for edit/delete/complete

### Task 6: Interactive Glow Effects
- [ ] Implement CSS variable-driven glow effects
- [ ] Add pointer tracking logic to cards
- [ ] Create GlowCard wrapper component
- [ ] Implement glow navigation tabs
- [ ] Add touch device fallbacks

### Task 7: Responsive Design
- [ ] Ensure layout adapts to mobile/desktop
- [ ] Optimize touch interactions for mobile
- [ ] Test responsive behavior across devices
- [ ] Adjust glow effects for different screen sizes

### Task 8: Testing & Validation
- [ ] Test authentication flows end-to-end
- [ ] Verify JWT tokens are properly attached to API requests
- [ ] Validate task CRUD operations work correctly
- [ ] Confirm glow effects work smoothly
- [ ] Test responsive behavior on different devices

---

## Risk Assessment

### High Priority Risks
- Security: Improper JWT handling could compromise user data
- Performance: Glow effects might cause layout thrashing or jank
- Compatibility: Better Auth integration might conflict with App Router

### Mitigation Strategies
- Strict security reviews of token handling code
- Performance profiling of glow effects with throttling if needed
- Thorough testing of auth integration with App Router

---

## Success Criteria

Implementation is complete when:
- Users can register and sign in via Better Auth
- JWT tokens are securely stored and attached to API requests
- All task management operations work correctly
- Glow effects enhance UI without impacting performance
- Application is responsive across desktop and mobile
- All authentication and task operations complete successfully
- Tests pass for all implemented functionality
- Glow effects work smoothly and are disabled on touch devices if needed