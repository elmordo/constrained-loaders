# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, TypeVar, List, Iterable, Sequence, Generic

T = TypeVar("T")


class DataSource(ABC, Generic[T]):
    @abstractmethod
    def load(self) -> List[T]:
        pass


class DataSourceBuilder(ABC, Generic[T]):
    @abstractmethod
    def build(self) -> DataSource[T]:
        pass


class DataSink(ABC, Generic[T]):
    @abstractmethod
    def save(self, items: Iterable[T]) -> None:
        pass

    @abstractmethod
    def delete(self, items: Iterable[T]) -> None:
        pass
