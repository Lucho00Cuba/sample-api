"""Security module."""

from typing import List
from fastapi import Depends, Request

from api.core import ApiHttpException
from .authentication import Authentication
from .authorization import Authorization


def get_current_user(request: Request):
    """Get the current user from the request headers."""
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise ApiHttpException(status_code=401, data="Authorization token missing")

    token = Authentication.extract_token_from_header(authorization)
    user_data = Authentication.verify_token(token)
    return user_data


def check_permissions(  # pylint: disable=dangerous-default-value
    current_user: dict = Depends(get_current_user),
    required_roles: List[str] = ["admin"],
):
    """Check if the user has the required roles."""
    user_roles = current_user["roles"]
    Authorization.authorize(user_roles, required_roles)
