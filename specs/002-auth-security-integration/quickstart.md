# Quickstart: Authentication & Security Integration

## Overview
This guide provides step-by-step instructions to set up the authentication and security layer using Better Auth (frontend) and JWT-based verification (backend).

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL database (Neon Serverless recommended)
- Git for version control
- Environment variables configured

## Frontend Setup (Next.js + Better Auth)

### 1. Install Dependencies
```bash
npm install better-auth @better-auth/react
```

### 2. Configure Better Auth Client
Create `src/lib/auth.ts`:
```typescript
import { createAuth } from "better-auth";

export const auth = createAuth({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
  secret: process.env.BETTER_AUTH_SECRET!,
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  // Enable JWT
  jwt: {
    secret: process.env.BETTER_AUTH_SECRET!,
    expiresIn: "15m", // 15 minutes for access token
    refreshExpiresIn: "7d", // 7 days for refresh token
  },
  // User configuration
  user: {
    account: {
      with: {
        email: true,
        username: true,
      },
    },
  },
});
```

### 3. Set Up Auth Provider
Create `src/components/auth-provider.tsx`:
```tsx
"use client";

import { AuthProvider } from "@better-auth/react";
import { auth } from "@/lib/auth";

export function AuthProviderWrapper({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider authClient={auth.client}>
      {children}
    </AuthProvider>
  );
}
```

### 4. Integrate with Layout
Update your main layout to include the auth provider:
```tsx
// src/app/layout.tsx
import { AuthProviderWrapper } from "@/components/auth-provider";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProviderWrapper>
          {children}
        </AuthProviderWrapper>
      </body>
    </html>
  );
}
```

## Backend Setup (FastAPI + JWT)

### 1. Install Dependencies
```bash
pip install python-jose[cryptography] passlib[bcrypt] fastapi uvicorn sqlmodel
```

### 2. Create JWT Utilities
Create `backend/src/core/security.py`:
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT scheme for dependency injection
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default 15 minutes

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

### 3. Create Authentication Dependency
Create `backend/src/api/deps.py`:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from ..core.security import security, verify_token
from ..models.user import User

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token"""
    token = credentials.credentials

    payload = verify_token(token)
    user_id: str = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    # In a real implementation, you would fetch user from database
    # For now, we return a user object with the ID from the token
    user = User(id=user_id, email=payload.get("email", ""), name=payload.get("name", ""))
    return user
```

### 4. Protect API Endpoints
Use the dependency in your API routes:
```python
from fastapi import APIRouter, Depends
from ..api.deps import get_current_user
from ..models.user import User

router = APIRouter()

@router.get("/protected-endpoint")
async def protected_route(current_user: User = Depends(get_current_user)):
    """This endpoint requires a valid JWT token"""
    return {"message": f"Hello {current_user.name}", "user_id": current_user.id}
```

## Environment Variables

### Frontend (.env.local)
```bash
NEXT_PUBLIC_BASE_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-key-here-at-least-32-characters-long
DATABASE_URL=your-database-url
```

### Backend (.env)
```bash
SECRET_KEY=your-super-secret-key-here-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=your-database-url
```

## Running the Application

### 1. Start Backend
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### 2. Start Frontend
```bash
cd frontend
npm run dev
```

## Testing Authentication

### 1. Register a New User
Send a POST request to `/auth/signup` with user details.

### 2. Login
Send a POST request to `/auth/signin` with credentials. This returns a JWT token.

### 3. Access Protected Endpoints
Include the JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Security Best Practices

### Token Management
- Store JWT tokens securely (preferably in HTTP-only cookies in production)
- Implement token refresh mechanisms
- Set appropriate expiration times
- Use HTTPS in production

### Error Handling
- Return consistent error responses for authentication failures
- Don't expose sensitive information in error messages
- Log authentication attempts for monitoring

### Secret Management
- Use environment variables for secrets
- Rotate secrets regularly
- Use different secrets for different environments