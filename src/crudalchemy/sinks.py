# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Iterable

from crudalchemy.types import DataSink, T


class DummySink(DataSink):
    def save(self, items: Iterable[T]) -> None:
        pass

    def delete(self, items: Iterable[T]) -> None:
        pass
