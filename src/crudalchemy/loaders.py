# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import List

from crudalchemy.types import DataSource, T


class DummySource(DataSource[T]):
    def load(self) -> List[T]:
        return []
