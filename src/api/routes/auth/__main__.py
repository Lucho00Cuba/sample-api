"""Auth module."""

from api.core import ApiResource
from api.security import Authentication
from api.schemas import User


class Register(ApiResource):  # pylint: disable=too-few-public-methods
    """Register resource."""

    def post(self, user: User):
        """Register a new user."""
        return Authentication.register_user(user.username, user.password)


class GetToken(ApiResource):  # pylint: disable=too-few-public-methods
    """GetToken resource."""

    def post(self, user: User):
        """Get a token for a user."""
        return Authentication.verify_user(user.username, user.password)
