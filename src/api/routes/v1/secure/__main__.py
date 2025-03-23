"""Secure module."""

from fastapi import Depends

from api.core import ApiResource, ApiResponse
from api.security import get_current_user


class V1Secure(ApiResource):  # pylint: disable=too-few-public-methods
    """Secure resource."""

    def get(self, current_user: dict = Depends(get_current_user)):
        """Get the secure resource."""
        return ApiResponse(
            status_code=200,
            data={"username": current_user["username"], "roles": current_user["roles"]},
        )
