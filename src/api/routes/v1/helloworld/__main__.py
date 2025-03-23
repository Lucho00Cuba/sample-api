"""HelloWorld module."""

from fastapi import Request
from fastapi_utils import set_responses

from pydantic import BaseModel

from api.core import ApiResource, ApiResponse


class HelloWorld(BaseModel):
    """HelloWorld model."""

    name: str


class V1HelloWorld(ApiResource):
    """Example resource with GET and POST methods."""

    @set_responses(ApiResponse)
    async def get(self) -> ApiResponse:
        """
        Handles GET requests.

        @returns
        - dict: A JSON response with a Hello World message.

        @example
        ```json
        {
            "message": "Hello, World!"
        }
        ```
        """
        return ApiResponse(status_code=200, data="Hello, World!")

    async def post(self, _: Request, hello_world: HelloWorld) -> ApiResponse:
        """
        Handles POST requests.

        @param request - The incoming HTTP request object.
        @param hello_world - The HelloWorld object containing the name.

        @returns
        - dict: A JSON response containing the Hello World message and optional request data.

        @example Request Body (JSON)
        ```json
        {
            "name": "John"
        }
        ```

        @example Response
        ```json
        {
            "status_code": 200,
            "data": "Hello, John!",
            "metatata": {
                "timestamp": "2023-07-11T16:00:00.000000+00:00"
            }
        }
        ```
        """
        status_code = 200
        data = f"Hello, {hello_world.name}!"

        return ApiResponse(status_code=status_code, data=data)
