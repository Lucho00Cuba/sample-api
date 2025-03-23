"""Test the HelloWorld endpoint."""

from fastapi.testclient import TestClient
from api import api

# Initialize the test client
app = api.app
client = TestClient(app)
PREFIX_PATH = "/apis"


# Test for the GET method
def test_hello_world_get():
    """Test the GET method."""
    response = client.get(f"{PREFIX_PATH}/v1/helloworld")
    assert response.status_code == 200
    assert response.json()["data"] == "Hello, World!"


# Test for the POST method without data (should fail because "name" is required)
def test_hello_world_post_without_name():
    """Test the POST method without data."""
    response = client.post(f"{PREFIX_PATH}/v1/helloworld")
    assert response.status_code == 422
    assert response.json()["data"] == [
        {"type": "missing", "loc": ["body"], "msg": "Field required", "input": None}
    ]


# Test for the POST method with valid data
def test_hello_world_post_with_name():
    """Test the POST method with valid data."""
    response = client.post(f"{PREFIX_PATH}/v1/helloworld", json={"name": "John"})
    assert response.status_code == 200
    assert response.json()["data"] == "Hello, John!"

    # Verify that the response contains metadata (timestamp)
    assert "metatata" in response.json()
    assert "timestamp" in response.json()["metatata"]


# Test for the POST method with invalid data (e.g., an unexpected value)
def test_hello_world_post_with_invalid_data():
    """Test the POST method with invalid data."""
    # Send an unexpected body, e.g., a value unrelated to "name"
    response = client.post(f"{PREFIX_PATH}/v1/helloworld", json={"age": 30})
    assert response.status_code == 422
    assert response.json()["data"] == [
        {
            "type": "missing",
            "loc": ["body", "name"],
            "msg": "Field required",
            "input": {"age": 30},
        }
    ]
