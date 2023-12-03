# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from abc import ABC
from typing import Generic, Optional, Any, Set, Iterable

from constrained_loaders.abstraction import (
    T,
    ConfigurableLoaderBuilder,
    LoaderSpec,
    Q,
    SortDirection,
)
from constrained_loaders.exceptions import (
    SortNotFound,
    FilterNotFound,
    ExtensionNotFound,
)


class LoaderBuilderBase(ConfigurableLoaderBuilder[T], ABC, Generic[T, Q]):
    """Base class for most loader builders. Provide system independent logic."""

    def __init__(self, spec: LoaderSpec[Q], bare_query: Q):
        """Initialize the library

        Args:
            spec: the loader spec
            bare_query: query without any constraints
        """
        self._spec: LoaderSpec[Q] = spec
        self._query = bare_query
        self._applied_extensions: Set[str] = set()
        self._sort_applied = False

    @property
    def loader_spec(self) -> LoaderSpec[Q]:
        """Get the loader spec"""
        return self._spec

    @property
    def is_any_sort_applied(self) -> bool:
        return self._sort_applied

    def apply_extension(self, extension_name: str) -> None:
        if extension_name in self._applied_extensions:
            # do not apply extension twice
            return
        try:
            extension = self._spec.extensions[extension_name]
        except KeyError:
            raise ExtensionNotFound(
                f"Extension '{extension_name}' not found in the spec"
            )
        self._applied_extensions.add(
            extension_name
        )  # it is first to avoid cycle in case of cyclic dependency
        try:
            self._apply_requirements(extension.required_extensions)
            self._query = extension.apply_extension(self._query)
        except Exception:
            self._applied_extensions.remove(extension_name)
            raise

    def add_sort(
        self, field: str, direction: SortDirection, options: Optional[Any] = None
    ):
        try:
            sort = self._spec.sortable_fields[field]
        except KeyError:
            raise SortNotFound(f"Sort field '{field}' not found in the spec")
        self._apply_requirements(sort.required_extensions)
        self._query = sort.apply_sorting(self._query, direction)
        self._sort_applied = True

    def add_filter(
        self, field: str, operator: str, reference_value: Optional[Any] = None
    ):
        try:
            available_filters = self._spec.filterable_fields[field]
            filter_ = available_filters[operator]
        except KeyError:
            raise FilterNotFound(
                f"Field '{field}' has no operator '{operator}' defined in the spec"
            )
        self._apply_requirements(filter_.required_extensions)
        self._query = filter_.apply_filter(self._query, reference_value)

    def _apply_requirements(self, requirements: Iterable[str]):
        """Apply set of requirement to the query"""
        for r in requirements:
            self.apply_extension(r)
