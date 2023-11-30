# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations


class ConstrainedLoadersException(Exception):
    """Base exception for all other exception defined in this library."""

    pass


class ExtensionNotFound(ConstrainedLoadersException, LookupError, KeyError):
    """Raised when extension was not found."""

    pass


class SortNotFound(ConstrainedLoadersException, LookupError, KeyError):
    """Raised when query sort was not found."""

    pass


class FilterNotFound(ConstrainedLoadersException, LookupError, KeyError):
    """Raised when filter was not found."""

    pass


class FieldNotDefined(ConstrainedLoadersException, LookupError, KeyError):
    """Raised when field was not found (e.g. no filter is defined for the field)."""

    pass
