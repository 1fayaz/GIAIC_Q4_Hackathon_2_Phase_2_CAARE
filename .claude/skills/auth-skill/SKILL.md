---
name: auth-skill
description: Design and implement secure authentication systems including signup, signin, password hashing, JWT tokens, and advanced auth integrations.
---

# Authentication Skill

## Instructions

1. **User Signup**
   - Validate input strictly (email, username, password)
   - Enforce strong password rules
   - Hash passwords before storage (never store plain text)
   - Prevent duplicate accounts
   - Return minimal success responses (avoid leaking info)

2. **User Signin**
   - Verify credentials securely
   - Use constant-time comparisons for passwords
   - Handle incorrect credentials without revealing details
   - Apply rate limiting and brute-force protection

3. **Password Security**
   - Use modern hashing algorithms (bcrypt, argon2, or scrypt)
   - Apply salting automatically
   - Never log or expose passwords
   - Support password reset flows using time-limited tokens

4. **JWT Tokens**
   - Issue short-lived access tokens
   - Use refresh tokens for session continuity
   - Store tokens securely (HTTP-only cookies preferred)
   - Validate token signature, issuer, audience, and expiration
   - Rotate and revoke tokens when necessary

5. **Enhanced Authentication Integration**
   - Integrate external auth providers or Better Auth correctly
   - Secure secrets and environment variables
   - Support role-based or permission-based authorization
   - Ensure compatibility with frontend and backend frameworks

## Best Practices
- Follow OWASP authentication guidelines
- Use HTTPS everywhere
- Prefer HTTP-only, Secure cookies over localStorage
- Implement CSRF protection when using cookies
- Log auth events without sensitive data
- Fail securely and explicitly
- Keep auth logic centralized and auditable

## Example Structure
```ts
// Signup
POST /auth/signup
- Validate input
- Hash password
- Store user
- Return success

// Signin
POST /auth/signin
- Verify credentials
- Issue JWT access & refresh tokens

// Protected Route
GET /profile
- Verify JWT
- Authorize user
- Return protected data
