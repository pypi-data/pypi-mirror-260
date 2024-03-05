"""
Shiro Python Client

This package provides convenient access to the Shiro API from applications written in the Python language.
"""

__version__ = "0.1.1"

from .client import ShiroClient
from .deployment import Deployment
from .prompt import Prompt
from .generate_completion import GenerateCompletion
# Import other classes as needed

__all__ = [
    "ShiroClient",
    "Deployment",
    "Prompt",
    "GenerateCompletion"
]
