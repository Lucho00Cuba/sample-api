"""Exceptions module."""

from typing import Any


class ApiHttpException(Exception):
    """Custom HTTPException for API responses."""

    def __init__(self, status_code: int, data: Any):
        self.status_code = status_code
        self.data = data
