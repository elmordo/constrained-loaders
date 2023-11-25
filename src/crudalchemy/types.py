# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Protocol, TypeVar, List, Iterable, Sequence

T = TypeVar("T")


class DataSource(Protocol[T]):

    def load(self) -> List[T]:
        pass


class DataSourceBuilder(Protocol[T]):

    def build(self) -> DataSource[T]:
        pass


class DataSink(Protocol[T]):

    def save(self, items: Iterable[T]) -> None:
        pass

    def delete(self, items: Iterable[T]) -> None:
        pass


class ExtraAction(Protocol[T]):

    def process(self, items: Sequence[T]) -> None:
        pass
