"""HelloWorld module."""

from fastapi import Request
from fastapi_utils import set_responses

from api.core import ApiResource, ApiResponse, ApiHttpException


class V1AlphaHelloWorld(ApiResource):
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
        return ApiResponse(status_code=200, data={"message": "Hello, World!"})

    async def post(self, request: Request):
        """
        Handles POST requests.

        @param request - The incoming HTTP request object.

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
            "message": "Hello, World!",
            "requests": {
                "name": "John"
            }
        }
        ```
        """
        r_msg = {"message": "Hello, World!"}
        try:
            data = request.json()
            if data:
                r_msg["requests"] = data
        except Exception as err:
            raise ApiHttpException(status_code=400, data=str(err)) from err
        return r_msg
