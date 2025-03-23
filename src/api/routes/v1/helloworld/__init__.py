"""HelloWorld module."""

from os import environ
from .__main__ import V1HelloWorld

publish = environ.get("V1_HELLOWORLD_PUBLISH", True)
