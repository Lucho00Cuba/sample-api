"""HelloWorld module."""

from os import environ
from .__main__ import V1AlphaHelloWorld

publish = environ.get("V1ALPHA_HELLOWORLD_PUBLISH", True)
