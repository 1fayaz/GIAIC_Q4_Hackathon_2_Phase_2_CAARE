"""
Authentication middleware for handling JWT token validation
"""
from fastapi import HTTPException, status
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from src.utils.security import get_current_user
from src.utils.jwt_utils import verify_token


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle JWT token validation for protected routes
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Define public routes that don't require authentication
        public_routes = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/api/auth/login",
            "/api/auth/register",
            "/"
        ]

        # Check if the current route is public
        is_public_route = any(request.url.path.startswith(route) for route in public_routes)

        # If it's not a public route, validate the token
        if not is_public_route:
            # Check for Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header missing or not in Bearer format"
                )

            # Extract token from header
            token = auth_header.split(" ")[1]

            # Verify the token
            payload = verify_token(token)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )

            # Add user info to request state for use in route handlers
            request.state.user = {
                "user_id": payload.get("sub"),
                "email": payload.get("email")
            }

        response = await call_next(request)
        return response


def get_current_user_from_request(request: Request):
    """
    Helper function to get current user from request state
    """
    if hasattr(request.state, 'user'):
        return request.state.user
    return None