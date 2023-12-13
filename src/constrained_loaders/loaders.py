# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Iterable

from constrained_loaders.abstraction import Loader, T


class DummyLoader(Loader[T]):
    """The dummy loader returns empty set of items"""

    def __iter__(self) -> Iterable[T]:
        return []

    def __len__(self) -> int:
        return 0
