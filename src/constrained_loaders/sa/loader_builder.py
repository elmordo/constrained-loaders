# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Generic

from sqlalchemy import Select
from sqlalchemy.orm import Session

from constrained_loaders import LoaderBuilderBase, T, LoaderSpec
from .loader import SALoader


class SALoaderBuilder(LoaderBuilderBase[T, Select], Generic[T]):
    def __init__(self, spec: LoaderSpec[Select], bare_query: Select, session: Session):
        super().__init__(spec, bare_query)
        self._session: Session = session

    def set_offset(self, offset: int) -> None:
        self._query = self._query.offset(offset)

    def set_limit(self, limit: int) -> None:
        self._query = self._query.limit(limit)

    def build(self) -> SALoader[T]:
        return SALoader(self._query, self._session)
