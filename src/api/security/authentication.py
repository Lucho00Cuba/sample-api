"""Authentication module."""

import datetime
from os import environ

import jwt
import pytz
from passlib.hash import bcrypt

from api.core import ApiHttpException, ApiResponse
from api.db import DBDriverFactory


class Authentication:
    """Authentication class."""

    secret = environ.get(
        "SECRET_KEY", "SECRET_KEY_PLACEHOLDER"
    )  # Replace with a real secret key
    tz = pytz.timezone("Europe/Madrid")

    # Instantiate the database driver
    db = DBDriverFactory.get_driver("local", "users.db.json")  # db_driver, db_filename

    @classmethod
    def generate_hash(cls, text: str) -> str:
        """Generate a hashed password"""
        return bcrypt.hash(text)

    @classmethod
    def verify_hash(cls, passwd: str, hashed: str) -> bool:
        """Verify if the password matches the hash"""
        return bcrypt.verify(passwd, hashed)

    @classmethod
    def generate_token(cls, username: str, roles: list) -> str:
        """Generate JWT token"""
        payload = {
            "iat": datetime.datetime.now(tz=cls.tz),
            "exp": datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=10),
            "username": username,
            "roles": roles,
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")

    @classmethod
    def verify_token(cls, token: str) -> dict:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, cls.secret, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError as err:
            raise ApiHttpException(status_code=401, data="Token has expired") from err
        except jwt.InvalidSignatureError as err:
            raise ApiHttpException(status_code=401, data="Token is invalid") from err
        except Exception as err:
            raise ApiHttpException(status_code=400, data=str(err)) from err

    @classmethod
    def extract_token_from_header(cls, authorization: str) -> str:
        """Extract token from Authorization header"""
        try:
            token = authorization.split(" ")[1]
            return token
        except IndexError as err:
            raise ApiHttpException(
                status_code=401, data="Authorization token missing"
            ) from err

    @classmethod
    def register_user(cls, username: str, password: str, roles: list = None) -> dict:
        """Register a new user"""
        if roles is None:
            roles = ["user"]  # Default role

        # Check if the user already exists in the database
        try:
            cls.db.read(username)
            raise ApiHttpException(
                status_code=400, data=f"User {username} already exists"
            )
        except KeyError:
            pass

        # Create a hash for the password
        hashed_password = cls.generate_hash(password)

        # Save the new user in the database
        user_data = {"password": hashed_password, "roles": roles}
        cls.db.create(username, user_data)

        return ApiResponse(status_code=200, data="User registered successfully")

    @classmethod
    def unregister_user(cls, username: str) -> dict:
        """Unregister (delete) a user"""
        # Remove the user from the database
        try:
            cls.db.delete(username)
            return {"message": "User unregistered successfully"}
        except KeyError as err:
            raise ApiHttpException(status_code=404, data="User not found") from err

    @classmethod
    def verify_user(cls, username: str, password: str) -> dict:
        """Verify a user by username and password"""
        try:
            user_data = cls.db.read(username)
        except KeyError as err:
            raise ApiHttpException(status_code=404, data="User not found") from err

        hashed_password = user_data["password"]
        if not cls.verify_hash(password, hashed_password):
            raise ApiHttpException(status_code=400, data="Invalid password")

        # Generate a token if credentials are correct
        token = cls.generate_token(username, user_data["roles"])
        return {"token": token}
