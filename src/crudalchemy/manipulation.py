# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Generic, List, Iterable, Optional, Callable

from .types import T, DataSource, DataSink


class Manipulator(Generic[T]):
    def __init__(
        self,
        item_factory: Callable[[], T],
        source: Optional[DataSource[T]] = None,
        sink: Optional[DataSink[T]] = None,
    ):
        self._items: list[T] = []
        self._item_factory: Callable[[], T] = item_factory
        self._source: DataSource[T] = source
        self._sink: DataSink[T] = sink

    def __iter__(self):
        return iter(self._items)

    def add_new(self):
        pass

    def extend(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def for_each(self):
        pass

    def map(self):
        pass

    def filter(self):
        pass

    def sort(self):
        pass
