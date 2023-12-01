# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from abc import ABC
from typing import Generic, Iterable, Self

from constrained_loaders.abstraction import LoaderBuilder, T


class DataSourceBuilderBase(LoaderBuilder[T], ABC, Generic[T]):
    def order_by(self, order_specs: Iterable) -> Self:
        return self
