# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import auto
from typing import (
    TypeVar,
    Iterable,
    Generic,
    Any,
    Optional,
    Self,
    Mapping,
    Sequence,
)

T = TypeVar("T")
"""Item type returned from a data source."""
Q = TypeVar("Q")
"""Query type internally used by a data source."""


class SortDirection:
    """Specify direction of sorting."""

    ASC = auto()
    """From the lowest to the highest value."""
    DESC = auto()
    """From the highest to the lowest value."""
    UNSPECIFIED = auto()
    """No direction modifier specified."""


class LoaderSpecPiece:
    """Represent piece of loader spec. Each loader piece have list of its requirement."""

    @abstractmethod
    @property
    def required_extensions(self) -> list[str]:
        """List of required extensions for this piece."""
        pass


class LoaderExtension(LoaderSpecPiece, ABC, Generic[Q]):
    """Represent loader extension (e.g. joins etc)."""

    @abstractmethod
    def apply_extension(self, query: Q) -> Q:
        """Apply the extension to the `query`."""
        pass


class QueryFilter(LoaderSpecPiece, ABC, Generic[Q]):
    """Apply filtration condition(s) to a query."""

    @abstractmethod
    def apply_filter(self, query: Q, reference_value: Optional[Any]) -> Q:
        """Apply the filtration condition specified by instance to the `query`."""
        pass


class QuerySort(LoaderSpecPiece, ABC, Generic[Q]):
    """Apply sorting to a query."""

    @abstractmethod
    def apply_sorting(self, query: Q, direction: SortDirection) -> Q:
        """Apply sorting to the `query`."""
        pass


@dataclass()
class DefaultSort:
    sort: str
    """Name of the sort field in the spec."""

    direction: SortDirection = SortDirection.UNSPECIFIED
    """Direction of sort."""

    @classmethod
    def from_string(cls, sort: str) -> Self:
        """Create instance from name of the sort field."""
        return cls(sort)


class DataSourceSpec(Generic[Q]):
    """Specification of available filters and sorts for loader."""

    sortable_fields: Mapping[str, QuerySort[Q]]
    """The key is field name and value is sort definition."""

    default_sort_by: Sequence[str | DefaultSort]
    """List of sorts used if no other sorts are specified."""

    filterable_fields: Mapping[str, Mapping[str, QueryFilter[Q]]]
    """Contain two nested mappings:
    
    The top level mapping is mapping from the field name (key) to lookup of operators (values).
    The second level mapping is operator lookup - the key is operator name (e.g. "eq", "lt", "like", ...) and value is
    instance of the `QueryFilter`.
    """

    extensions: Mapping[str, LoaderExtension[Q]]
    """The key is extension name and value is extension itself."""


class DataSource(ABC, Generic[T]):
    """Base class for all data sources."""

    @abstractmethod
    def __next__(self) -> T:
        """Iterate over"""

    @abstractmethod
    def __len__(self) -> int:
        """Get total count of items available in the loader"""


class DataSourceBuilder(ABC, Generic[T]):
    """Create instances of the data sources."""

    @abstractmethod
    def build(self) -> DataSource[T]:
        """Build new `DataSource` instance."""
        pass


class MutableDataSourceBuilder(ABC, Generic[T]):
    """Extend the `DataSourceBuilder` by build configuration methods."""

    @abstractmethod
    def add_sort(
        self, field: str, direction: SortDirection, options: Optional[Any] = None
    ):
        """Add sort requirement to the configuration."""
        pass

    @abstractmethod
    def add_filter(
        self, field: str, operator: str, reference_value: Optional[Any] = None
    ):
        """Add filter requirement to the configuration."""
        pass

    @abstractmethod
    def set_offset(self, offset: int):
        """Set offset in row set where to start."""
        pass

    @abstractmethod
    def set_limit(self, limit: int):
        """Set max number of items to be returned."""
        pass

    def set_page(self, page: int, items_per_page: int):
        """Shorthand for calling `set_offset` and `set_limit` method when using pagination."""
        self.set_limit(items_per_page)
        self.set_offset(page * items_per_page)


class DataSink(ABC, Generic[T]):
    """Modify a data storage."""

    @abstractmethod
    def save(self, items: Iterable[T]) -> None:
        """Save items to the storage."""
        pass

    @abstractmethod
    def delete(self, items: Iterable[T]) -> None:
        """Delete items from the storage."""
        pass
