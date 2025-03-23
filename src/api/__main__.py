"""Server module."""

import uvicorn

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.core import Api, ApiResponse, ApiHttpException

api = Api()


@api.app.get("/")
def home():
    """
    Home endpoint

    Returns:
        dict: A JSON response with a message.
    """
    return {"message": "Hello World"}


@api.app.middleware("http")
async def after_request(request: Request, call_next):
    """
    Middleware to add custom headers to the response.

    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable): The next middleware function in the chain.

    Returns:
        Response: The response object with the custom headers added.
    """
    response = await call_next(request)
    response.headers["X-Backend"] = "Sample API"
    return response


@api.app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(_: Request, exc: StarletteHTTPException):
    """
    Exception handler for StarletteHTTPException.

    Args:
        _ (Request): The incoming HTTP request.
        exc (StarletteHTTPException): The StarletteHTTPException instance.

    Returns:
        Response: A JSON response with the status code and data.
    """
    api.app.logger.error("StarletteHTTPException: %s", exc)
    response = ApiResponse(status_code=exc.status_code, data=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=response.to_dict())


@api.app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    """
    Exception handler for RequestValidationError.

    Args:
        _ (Request): The incoming HTTP request.
        exc (RequestValidationError): The RequestValidationError instance.

    Returns:
        Response: A JSON response with the status code and data.
    """
    api.app.logger.error("RequestValidationError: %s", exc)
    response = ApiResponse(status_code=422, data=exc.errors())
    return JSONResponse(status_code=422, content=response.to_dict())


@api.app.exception_handler(ApiHttpException)
async def http_exception_handler(_: Request, exc: ApiHttpException):
    """
    Exception handler for ApiHttpException.

    Args:
        _ (Request): The incoming HTTP request.
        exc (ApiHttpException): The ApiHttpException instance.

    Returns:
        Response: A JSON response with the status code and data.
    """
    if hasattr(exc, "__cause__"):
        api.app.logger.error("ApiHttpException: %s", exc.__cause__)
    response = ApiResponse(status_code=exc.status_code, data=exc.data)
    return JSONResponse(status_code=exc.status_code, content=response.to_dict())


@api.app.exception_handler(Exception)
async def all_exception_handler(_: Request, exc: Exception):
    """
    Logging for all other exceptions.

    Args:
        _ (Request): The incoming HTTP request.
        exc (Exception): The Exception instance.

    Returns:
        Response: A JSON response with the status code and data.
    """
    api.app.logger.error("Exception: %s", exc)
    response = ApiResponse(status_code=500, data="Internal Server Error")
    return JSONResponse(status_code=500, content=response.to_dict())


def run():
    """Method to start the server."""
    uvicorn.run(
        "api.__main__:api.app",
        host=api.HOST,
        port=api.PORT,
        reload=api.IS_DEV,
        server_header=False,
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "default": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "loggers": {
                "uvicorn": {
                    "level": "INFO",
                    "handlers": ["default"],
                    "propagate": False,
                },
                "uvicorn.error": {
                    "level": "INFO",
                    "handlers": ["default"],
                    "propagate": False,
                },
                "uvicorn.access": {
                    "level": "INFO",
                    "handlers": ["default"],
                    "propagate": False,
                },
            },
        },
    )


if __name__ == "__main__":
    api.app.logger.info("API Initialized")
    run()
