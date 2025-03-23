"""Test the exception handlers."""

from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException as StarletteHTTPException
from api.core import ApiHttpException
from api import api

app = api.app
client = TestClient(app)


def test_starlette_http_exception_handler():
    """Test the StarletteHTTPException handler."""

    # Register a route that will raise a StarletteHTTPException (e.g., 404 Not Found)
    @app.get("/trigger-starlette-http-error")
    async def trigger_starlette_http_error():
        raise StarletteHTTPException(status_code=404, detail="Not Found")

    # Simulate a request to the endpoint that raises the exception
    response = client.get("/trigger-starlette-http-error")

    # Check if the status code is 404 as expected
    assert response.status_code == 404

    # Check if the response data contains the error message
    assert "Not Found" in response.json()["data"]


def test_api_http_exception_handler():
    """Test the ApiHttpException handler."""

    # Register a route that will raise the ApiHttpException
    @app.get("/trigger-api-error")
    async def trigger_api_error():
        raise ApiHttpException(status_code=400, data="Custom error message")

    # Simulate a request to the endpoint that raises the exception
    response = client.get("/trigger-api-error")

    # Check if the status code is 400 as expected
    assert response.status_code == 400

    # Check if the response data contains the custom error message
    assert "Custom error message" in response.json()["data"]


def test_request_validation_exception_handler():
    """Test the RequestValidationError handler."""

    # Register a route that expects a query parameter and simulates validation error
    @app.get("/trigger-validation-error")
    async def trigger_validation_error(q: str):  # pylint: disable=unused-argument
        return {"message": "This won't be reached if validation fails"}

    # Simulate a request to the endpoint without the required query parameter
    response = client.get("/trigger-validation-error")

    # Check if the status code is 422 (Validation failed)
    assert response.status_code == 422
