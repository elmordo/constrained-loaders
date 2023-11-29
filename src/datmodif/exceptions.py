# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations


class DatmodifException(Exception):
    """Base exception for all other exception defined in this library."""

    pass


class ExtensionNotFound(DatmodifException, LookupError, KeyError):
    """Raised when extension was not found."""

    pass


class SortNotFound(DatmodifException, LookupError, KeyError):
    """Raised when query sort was not found."""

    pass


class FilterNotFound(DatmodifException, LookupError, KeyError):
    """Raised when filter was not found."""

    pass


class FieldNotDefined(DatmodifException, LookupError, KeyError):
    """Raised when field was not found (e.g. no filter is defined for the field)."""

    pass
