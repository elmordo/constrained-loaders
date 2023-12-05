# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Generic

from sqlalchemy import Select
from sqlalchemy.orm import Session

from constrained_loaders import LoaderBuilderBase, T, LoaderSpec
from constrained_loaders.sa.loader import SALoader


class BuiltQuery:
    def build_select(self) -> Select:
        raise NotImplementedError()


class SAComplexLoaderBuilder(LoaderBuilderBase[T, BuiltQuery], Generic[T]):
    def __init__(
        self, spec: LoaderSpec[BuiltQuery], bare_query: BuiltQuery, session: Session
    ):
        super().__init__(spec, bare_query)
        self._session = session
        self._offset: int | None = None
        self._limit: int | None = None

    def set_offset(self, offset: int | None) -> None:
        self._offset = offset

    def set_limit(self, limit: int | None) -> None:
        self._limit = limit

    def build(self) -> SALoader[T]:
        s = self._query.build_select()
        if self._limit is not None:
            s = s.limit(self._limit)
        if self._offset is not None:
            s = s.offset(self._offset)
        return SALoader(s, self._session)
