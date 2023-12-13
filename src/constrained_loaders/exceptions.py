# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations


class ConstrainedLoadersException(Exception):
    """Base exception for all other exception defined in this library."""

    pass


class ExtensionNotFound(ConstrainedLoadersException, KeyError):
    """Raised when extension was not found."""

    pass


class SortNotFound(ConstrainedLoadersException, KeyError):
    """Raised when query sort was not found."""

    pass


class FilterNotFound(ConstrainedLoadersException, KeyError):
    """Raised when filter was not found."""

    pass


class InvalidBuilderConfigurationException(ConstrainedLoadersException):
    """Raised from LoaderBuilder.build() method in case of invalid configuration (some fields are missing, etc.)"""

    pass
