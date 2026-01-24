# Research: Frontend UI, Auth & Interactive Effects

**Feature**: 003-frontend-auth-integration
**Date**: 2026-01-22
**Author**: Claude Code

## Next.js App Router Best Practices

### Decision: Use conventional folder structure with layout nesting
**Rationale**: Next.js App Router follows convention-over-configuration approach, making it easier to understand and maintain
**Alternatives considered**: Custom routing libraries, Pages Router (not compatible with requirements)

### Decision: Implement loading states with Suspense boundaries
**Rationale**: Provides better user experience during data fetching
**Alternatives considered**: Custom loading spinners, skeleton screens

## Better Auth Integration Patterns

### Decision: Use Better Auth with JWT token handling in Next.js App Router
**Rationale**: Aligns with security requirements and backend JWT verification
**Alternatives considered**: Traditional session cookies (violates JWT requirement), custom auth solutions (higher complexity)

### Decision: Store JWT tokens in httpOnly cookies for security
**Rationale**: Prevents XSS attacks while allowing seamless auth state management
**Alternatives considered**: Local storage (vulnerable to XSS), memory storage (lost on refresh)

## Glow Effect Implementation Approaches

### Decision: Use CSS variables and pseudo-elements for glow effects
**Rationale**: Pure CSS solution that doesn't require canvas or WebGL as specified
**Alternatives considered**: Canvas-based effects (overkill, not allowed), SVG filters (complex positioning)

### Decision: Implement pointer tracking with requestAnimationFrame for performance
**Rationale**: Provides smooth animations while maintaining performance
**Alternatives considered**: Event listeners without rAF (potential jank), CSS hover effects (limited interaction)

## Shadcn UI Integration

### Decision: Configure Shadcn UI with Tailwind CSS and TypeScript
**Rationale**: Provides accessible, customizable components that follow best practices
**Alternatives considered**: Building components from scratch (time-intensive), other component libraries (different ecosystems)

## API Client Architecture

### Decision: Create centralized API client with interceptors
**Rationale**: Ensures consistent request handling and error management
**Alternatives considered**: Direct fetch calls (duplication), third-party libraries (dependency overhead)

### Decision: Implement automatic token refresh mechanism
**Rationale**: Maintains user sessions without interruption
**Alternatives considered**: Manual refresh prompts (poor UX), no refresh (frequent re-authentication)