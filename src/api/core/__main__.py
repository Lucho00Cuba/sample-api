"""API module."""

import sys
import logging
import importlib
import ast
from datetime import datetime
from os import environ, walk, path
from typing import Any, Dict
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_utils import Api as FastRestApi
from fastapi_utils import Resource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Api:  # pylint: disable=too-few-public-methods
    """Base class to handle automatic route registration."""

    __path_module = "/".join(__file__.split("/")[:-2])

    HOST = environ.get("API_HOST", "0.0.0.0")
    PORT = int(environ.get("API_PORT", 3000))
    IS_DEV = environ.get("API_IS_DEV", "false").lower() == "true"
    app = FastAPI(title="API", version="0.1.0", description="SAMPLE API")
    app.logger = logging.getLogger("api")
    logging.basicConfig(level=logging.INFO)
    api = FastRestApi(app)

    app.logger.info("Host: %s", HOST)
    app.logger.info("Port: %s", PORT)
    app.logger.info("IsDev: %s", IS_DEV)

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Api, cls).__new__(cls, *args, **kwargs)
            cls._instance._load_paths()
        return cls._instance

    # def __init__(self):
    #     self._load_paths()

    @staticmethod
    def _get_time():
        """Get the current time."""
        date_time = datetime.now()
        return date_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    def get_first_class_name_from_init(self, file_path: str) -> str:
        """Get the first class name from the __init__.py file."""
        init_file_path = path.join(file_path, "__init__.py")

        if not path.exists(init_file_path):
            raise FileNotFoundError(f"{init_file_path} does not exist.")

        with open(init_file_path, "r", encoding="utf-8") as f:
            # Read the content of the __init__.py file
            file_content = f.read()

        # Parse the file content into an Abstract Syntax Tree (AST)
        tree = ast.parse(file_content)

        # Traverse the AST nodes and look for the first class definition
        for node in tree.body:
            if isinstance(node, ast.ImportFrom):  # This is an import statement
                # Check if the class is imported (not just a module)
                for alias in node.names:
                    # Return the name of the class being imported
                    if node.module == "__main__":
                        return alias.name

        # If no class was found, return None or a default value
        return None

    def _load_paths(self):
        """Method to load the API paths."""
        try:
            self.app.logger.info("Loading routes")
            sys.path.append(f"{self.__path_module}/routes")
            for dirname, _, files in walk(f"{self.__path_module}/routes"):
                module_path_segments = dirname.strip("/").split("/")
                base_path_segments = self.__path_module.strip("/").split("/")
                base_path_segments.append("routes")

                if "__main__.py" not in files:
                    continue

                result = [
                    segment
                    for segment in module_path_segments
                    if segment not in base_path_segments
                ]
                if result:
                    module_name = ".".join(result)
                    self.app.logger.info("Filename routes/%s", "/".join(result))
                    self.app.logger.info("Loading %s", module_name)

                    pathRoute = (  # pylint: disable=invalid-name
                        f'/apis/{"/".join(result)}'
                    )
                    self.app.logger.info("Route %s", pathRoute)

                    module = importlib.import_module(module_name)

                    if hasattr(module, "publish"):
                        if not module.publish:
                            self.app.logger.info("Skipping Publish %s", pathRoute)
                            continue

                    if hasattr(module, "resources"):
                        for resource in module.resources:
                            pathRoute = resource[0]  # pylint: disable=invalid-name
                            import_class = resource[1]
                            self.app.logger.info("Resource %s", import_class.__name__)
                            self.api.add_resource(import_class(), pathRoute)
                            self.app.logger.info("Publish %s", pathRoute)
                    else:
                        className = self.get_first_class_name_from_init(  # pylint: disable=invalid-name
                            dirname
                        )
                        if not className:
                            self.app.logger.error("No class found in %s", dirname)
                            continue
                        self.app.logger.info("ClassName %s", className)
                        import_class = getattr(module, className)

                        self.api.add_resource(import_class(), pathRoute)
                        self.app.logger.info("Publish %s", pathRoute)

        except Exception as err:  # pylint: disable=broad-except
            self.app.logger.error(err)


class ApiResponse(BaseModel):  # pylint: disable=too-few-public-methods
    """Base class for API responses."""

    data: Any
    status_code: int
    metatata: dict = {"timestamp": Api._get_time()}  # pylint: disable=protected-access

    def to_dict(self):
        """Convert the model to a dict for FastAPI."""
        response = self.model_dump()
        return response

    def __json__(self) -> Dict[str, Any]:
        """
        Override this method to automatically convert the model to a dict for FastAPI.

        Returns:
            dict: A dictionary representation of the ApiResponse object.
        """
        # Use model_dump to get a dict of the fields
        response = self.model_dump()
        return response


class ApiResource(Resource):  # pylint: disable=too-few-public-methods
    """Base class for API resources."""
