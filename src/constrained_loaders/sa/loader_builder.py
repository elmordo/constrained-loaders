# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Generic

from sqlalchemy import Select

from constrained_loaders import LoaderBuilderBase, Loader, T


class SALoaderBuilder(LoaderBuilderBase[T, Select], Generic[T]):
    def set_offset(self, offset: int) -> None:
        self._query = self._query.offset(offset)

    def set_limit(self, limit: int) -> None:
        self._query = self._query.limit(limit)

    def build(self) -> Loader[T]:
        pass
