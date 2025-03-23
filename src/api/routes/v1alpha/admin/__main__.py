"""Admin module."""

from typing import List
from fastapi import Depends

from api.core import ApiResource, ApiResponse
from api.security import get_current_user


class V1AlphaAdmin(ApiResource):  # pylint: disable=too-few-public-methods
    """Admin resource."""

    def get(
        self,
        current_user: dict = Depends(get_current_user),
        required_roles: List[str] = Depends(lambda: ["admin"]),
    ):
        """Get the admin resource."""
        return ApiResponse(
            status_code=200,
            data={
                "username": current_user["username"],
                "roles": current_user["roles"],
                "required_roles": required_roles,
            },
        )
