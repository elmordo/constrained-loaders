# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Generic, Iterable, Optional, Callable, Any

from .abstraction import T, DataSource, DataSink


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

    def __len__(self) -> int:
        return len(self._items)

    def append_new(self) -> None:
        """Append new item to manipulator.

        Only further operations will affect the new item.
        """
        self._items.append(self._item_factory())

    def extend(self, items: Iterable[T]) -> None:
        """Append many items from given param to the managed items."""
        self._items.extend(items)

    def set_property(self, key: str, val: Any):
        """Set property value on all managed items"""
        for item in self._items:
            setattr(item, key, val)

    def save(self):
        self._sink.save(self._items)

    def delete(self):
        self._sink.delete(self._items)

    def for_each(self, callback: Callable[[T], None]):
        for item in self._items:
            callback(item)

    def filter(self, filter_fn: Callable[[T], bool]):
        self._items = list(filter(filter_fn, self._items))

    def sort(self, compare_fn: Callable[[T, T], int]):
        self._items.sort(key=compare_fn)
