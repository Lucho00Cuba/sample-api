"""Test the home endpoint."""

from fastapi.testclient import TestClient
from api.core import Api

# Initialize the API and the TestClient
api = Api()
app = api.app
client = TestClient(app)


def test_home():
    """Test the home endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
