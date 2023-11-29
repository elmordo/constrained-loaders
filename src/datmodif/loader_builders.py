# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from abc import ABC
from typing import Generic, Iterable, Self

from crudalchemy.abstraction import DataSourceBuilder, T


class DataSourceBuilderBase(DataSourceBuilder[T], ABC, Generic[T]):
    def order_by(self, order_specs: Iterable) -> Self:
        return self
