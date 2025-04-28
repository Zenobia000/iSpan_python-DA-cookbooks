"""
Utility module for the Python OOP Course.

This package provides helper functions and custom exceptions
for the Python Object-Oriented Programming course.
"""

__version__ = '0.1.0'
__author__ = 'iSpan Python DA Team'

from .helper_functions import (
    get_project_root,
    create_timestamp,
    format_output
)

from .custom_exceptions import (
    ValidationError,
    ResourceNotFoundError,
    AuthorizationError
)

__all__ = [
    'get_project_root',
    'create_timestamp',
    'format_output',
    'ValidationError',
    'ResourceNotFoundError',
    'AuthorizationError'
] 