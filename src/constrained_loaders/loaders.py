# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from constrained_loaders.abstraction import Loader, T


class DummyLoader(Loader[T]):
    def __next__(self) -> T:
        return []

    def __len__(self) -> int:
        return 0
