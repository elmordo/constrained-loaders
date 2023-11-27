# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import auto
from typing import TypeVar, List, Iterable, Generic, Any

T = TypeVar("T")


class DataSource(ABC, Generic[T]):
    """Base class for all data sources."""

    @abstractmethod
    def load(self) -> List[T]:
        """Get all data from data source."""
        pass


class OrderDirection:
    """Specify direction of sorting"""

    ASC = auto()
    """From the lowest to the highest value"""
    DESC = auto()
    """From the highest to the lowest value"""
    UNSPECIFIED = auto()
    """No direction modifier specified"""


@dataclass()
class OrderSpec:
    """Specify one sorting expression"""

    field: str
    """Name of the sortable field"""
    direction: OrderDirection = OrderDirection.UNSPECIFIED
    """Sort direction spec"""
    options: Any = None
    """Implementation specific options (e.g. NULLS FIRST)"""


@dataclass
class FilterSpec:
    field: str
    """The field name"""
    operator: str
    """Operator name"""
    reference_value: str | None = None
    """Reference value (for unary operators could be `None`)"""


class DataSourceBuilder(ABC, Generic[T]):
    @abstractmethod
    def build(self) -> DataSource[T]:
        pass


class MutableDataSourceBuilder(ABC, Generic[T]):
    @abstractmethod
    def add_order_by(self, order_spec: OrderSpec):
        pass

    @abstractmethod
    def add_filter(self, filter_spec: FilterSpec):
        pass

    @abstractmethod
    def set_offset(self, offset: int):
        pass

    @abstractmethod
    def set_limit(self, limit: int):
        pass

    @abstractmethod
    def set_page(self, page: int, items_per_page: int):
        pass


class DataSink(ABC, Generic[T]):
    @abstractmethod
    def save(self, items: Iterable[T]) -> None:
        pass

    @abstractmethod
    def delete(self, items: Iterable[T]) -> None:
        pass
