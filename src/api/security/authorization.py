"""Authorization module."""

from typing import List

from api.core import ApiHttpException


class Authorization:
    """Authorization class."""

    @classmethod
    def has_permission(cls, roles: List[str], required_roles: List[str]) -> bool:
        """Check if the user has any of the required roles"""
        return any(role in required_roles for role in roles)

    @classmethod
    def authorize(cls, user_roles: List[str], required_roles: List[str]):
        """Check if the user has permissions to access the resource"""
        if not cls.has_permission(user_roles, required_roles):
            raise ApiHttpException(
                status_code=403, data="User does not have sufficient permissions"
            )
