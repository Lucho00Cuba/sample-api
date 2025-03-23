"""Auth module."""

from .__main__ import Register, GetToken

resources = [
    ["/auth/register", Register],
    ["/auth/login", GetToken],
    ["/auth/get-token", GetToken],
]
