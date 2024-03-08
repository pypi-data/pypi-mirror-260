"""Exceptions for Arve"""

from typing import Any


class ArveError(Exception):
    """Generic Arve exception"""


class ArveConnectionError(ArveError):
    """Arve connection exception"""


class ArveUnathorizedError(ArveError):
    """Arve unauthorized exception"""
