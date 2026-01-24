"""
Authorization service for handling user permissions and access control
"""
from typing import Dict, Optional


class AuthZService:
    """
    Service class for handling authorization and access control operations
    """

    @staticmethod
    def check_user_owns_resource(current_user: Dict, resource_owner_id: str) -> bool:
        """
        Check if the current user owns the specified resource

        Args:
            current_user: Dictionary containing current user information
            resource_owner_id: ID of the resource owner

        Returns:
            True if the user owns the resource, False otherwise
        """
        return current_user.get("user_id") == resource_owner_id

    @staticmethod
    def check_user_permission(current_user: Dict, required_permission: str) -> bool:
        """
        Check if the current user has the required permission

        Args:
            current_user: Dictionary containing current user information
            required_permission: Permission required to access the resource

        Returns:
            True if the user has the required permission, False otherwise
        """
        # In a basic implementation, we can check user roles or permissions
        # For now, we'll just return True for any permission check
        # In a real implementation, you would check user roles/permissions
        user_permissions = current_user.get("permissions", [])
        return required_permission in user_permissions

    @staticmethod
    def check_resource_access(current_user: Dict, resource: Dict, action: str = "read") -> bool:
        """
        Check if the current user has access to the specified resource for the given action

        Args:
            current_user: Dictionary containing current user information
            resource: Dictionary containing resource information
            action: Action to be performed (read, write, delete, etc.)

        Returns:
            True if the user has access, False otherwise
        """
        # Check if user owns the resource
        resource_owner_id = resource.get("user_id") or resource.get("owner_id")
        if resource_owner_id:
            return AuthZService.check_user_owns_resource(current_user, resource_owner_id)

        # If no owner specified, check general permissions
        required_permission = f"{action}_{resource.get('type', 'resource')}"
        return AuthZService.check_user_permission(current_user, required_permission)

    @staticmethod
    def filter_user_resources(resources: list, current_user: Dict) -> list:
        """
        Filter a list of resources to only include those owned by the current user

        Args:
            resources: List of resource dictionaries
            current_user: Dictionary containing current user information

        Returns:
            List of resources owned by the current user
        """
        user_id = current_user.get("user_id")
        return [
            resource for resource in resources
            if resource.get("user_id") == user_id or resource.get("owner_id") == user_id
        ]