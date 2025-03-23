"""Test the authentication endpoints."""

from unittest.mock import patch
from fastapi.testclient import TestClient
from api.core import ApiHttpException
from api.security import Authentication
from api import api


# Initialize the test client
app = api.app
client = TestClient(app)


# Test for the Register endpoint (POST)
def test_register_user():
    """Test the Register endpoint (POST)."""
    # Mock the behavior of Authentication.register_user to simulate successful registration
    with patch.object(
        Authentication,
        "register_user",
        return_value={"message": "User registered successfully"},
    ) as mock_register:
        # Prepare user data
        user_data = {"username": "testuser", "password": "password123"}

        # Send POST request to the /register endpoint
        response = client.post("/auth/register", json=user_data)

        # Verify the status code and response content
        assert response.status_code == 200
        assert response.json() == {"message": "User registered successfully"}

        # Verify that the register_user method was called with the correct parameters
        mock_register.assert_called_once_with(
            user_data["username"], user_data["password"]
        )


# Test for the GetToken endpoint (POST) - success case
def test_get_token_success():
    """Test the GetToken endpoint (POST) - success case."""
    # Mock the behavior of Authentication.verify_user to simulate successful token generation
    with patch.object(
        Authentication, "verify_user", return_value={"token": "valid_token"}
    ) as mock_verify:
        # Prepare user data
        user_data = {"username": "testuser", "password": "password123"}

        # Send POST request to the /get-token endpoint
        response = client.post("/auth/get-token", json=user_data)

        # Verify the status code and response content
        assert response.status_code == 200
        assert "token" in response.json()

        # Verify that the verify_user method was called with the correct parameters
        mock_verify.assert_called_once_with(
            user_data["username"], user_data["password"]
        )


# Test for the GetToken endpoint (POST) - invalid credentials
def test_get_token_invalid_credentials():
    """Test the GetToken endpoint (POST) - invalid credentials."""
    # Mock the behavior of Authentication.verify_user to simulate invalid credentials
    with patch.object(
        Authentication,
        "verify_user",
        side_effect=ApiHttpException(status_code=400, data="Invalid password"),
    ):
        # Prepare user data with invalid credentials
        user_data = {"username": "wronguser", "password": "wrongpassword"}

        # Send POST request to the /get-token endpoint
        response = client.post("/auth/get-token", json=user_data)

        # Verify the status code is 400 (invalid credentials)
        assert response.status_code == 400

        # Verify that the response contains the error message
        assert response.json()["data"] == "Invalid password"


# Test for the Register endpoint (POST) - missing fields
def test_register_user_missing_fields():
    """Test the Register endpoint (POST) - missing fields."""
    # Send POST request to the /register endpoint with missing fields
    user_data = {"username": "testuser"}  # Missing password
    response = client.post("/auth/register", json=user_data)

    # Verify the status code and response content
    assert response.status_code == 422  # Unprocessable Entity (validation error)
    assert "data" in response.json()
    assert response.json()["data"] == [
        {
            "type": "missing",
            "loc": ["body", "password"],
            "msg": "Field required",
            "input": {"username": "testuser"},
        }
    ]


# Test for the GetToken endpoint (POST) - missing fields
def test_get_token_missing_fields():
    """Test the GetToken endpoint (POST) - missing fields."""
    # Send POST request to the /get-token endpoint with missing fields
    user_data = {"username": "testuser"}  # Missing password
    response = client.post("/auth/get-token", json=user_data)

    # Verify the status code and response content
    assert response.status_code == 422  # Unprocessable Entity (validation error)
    assert "data" in response.json()
    assert response.json()["data"] == [
        {
            "type": "missing",
            "loc": ["body", "password"],
            "msg": "Field required",
            "input": {"username": "testuser"},
        }
    ]
