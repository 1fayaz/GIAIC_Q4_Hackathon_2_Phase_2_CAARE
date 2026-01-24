# Quickstart Guide: Frontend UI, Auth & Interactive Effects

**Feature**: 003-frontend-auth-integration
**Date**: 2026-01-22
**Author**: Claude Code

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Git
- Access to backend API (FastAPI server running)

### Step 1: Initialize Next.js Project
1. Create new Next.js project with TypeScript:
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
   ```
2. Navigate to project directory:
   ```bash
   cd frontend
   ```

### Step 2: Install Dependencies
1. Install Shadcn UI components:
   ```bash
   npx shadcn@latest init
   npx shadcn@latest add button card form input label
   ```
2. Install Better Auth:
   ```bash
   npm install better-auth
   ```
3. Install additional dependencies:
   ```bash
   npm install lucide-react
   ```

### Step 3: Configure Better Auth
1. Set up Better Auth provider in your app
2. Configure environment variables for JWT settings
3. Verify JWT compatibility with backend

### Step 4: Set Up API Client
1. Create centralized API client with JWT interceptor
2. Implement automatic Authorization header injection
3. Add error handling and loading states

### Step 5: Create Component Structure
1. Build auth components (sign-in, sign-up forms)
2. Create task management components (cards, forms, lists)
3. Implement glow effect components using CSS variables

### Step 6: Implement App Router Structure
1. Set up protected and public routes
2. Create layout hierarchy with auth and app layouts
3. Implement navigation with glow effects

### Step 7: Add Interactive Effects
1. Implement CSS variable-driven glow effects
2. Add pointer tracking with performance optimization
3. Test touch device compatibility

### Step 8: Test Integration
1. Verify auth flow works with backend
2. Test JWT token handling
3. Validate task CRUD operations
4. Confirm responsive behavior

## Configuration Values

### Environment Variables
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL
- `NEXT_PUBLIC_JWT_SECRET`: JWT verification secret (synced with backend)
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Better Auth endpoint

### Package Versions
- Next.js: 14+ (compatible with App Router)
- TypeScript: 5+
- Tailwind CSS: 3+
- Better Auth: Latest stable

## Common Issues and Solutions

### Issue: JWT token not attaching to requests
**Solution**: Verify API client interceptor is properly configured with Authorization header

### Issue: Glow effects causing performance issues
**Solution**: Implement requestAnimationFrame and throttling for pointer tracking

### Issue: Auth state not persisting across page reloads
**Solution**: Verify token storage implementation (cookies vs localStorage)

### Issue: CORS errors with backend API
**Solution**: Ensure proper CORS configuration in both frontend and backend

## Testing Commands

### Development Server
```bash
npm run dev
```

### Build Process
```bash
npm run build
```

### Linting
```bash
npm run lint
```

### Manual Testing
1. Test authentication flow (sign-up, sign-in, protected routes)
2. Verify task CRUD operations work with backend
3. Confirm glow effects work smoothly without jank
4. Test responsive behavior on mobile/desktop
5. Validate JWT token handling and expiration