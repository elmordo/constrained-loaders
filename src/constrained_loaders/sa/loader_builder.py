# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Generic, Dict, Optional, Any

from sqlalchemy import Select
from sqlalchemy.orm import Session

from constrained_loaders import (
    LoaderBuilderBase,
    T,
    LoaderSpec,
    QuerySort,
    SortDirection,
    QueryFilter,
    QueryExtension,
)
from constrained_loaders.sa.loader import SALoader


class SALoaderBuilderContext:
    def __init__(self, initial_select: Select):
        self.main_query = initial_select
        self.sub_queries: Dict[str, Select] = {}
        self._filters = []
        self._sorts = []

    def add_filter(self, filter_):
        self._filters.append(filter_)

    def add_sort(self, sort_):
        self._sorts.append(sort_)

    def build_select(self) -> Select:
        raise NotImplementedError()


class SALoaderBuilder(LoaderBuilderBase[T, SALoaderBuilderContext], Generic[T]):
    def __init__(
        self,
        spec: LoaderSpec[SALoaderBuilderContext],
        bare_query: SALoaderBuilderContext,
        session: Session,
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


class SAQuerySort(QuerySort[SALoaderBuilderContext]):
    def apply_sorting(
        self, context: SALoaderBuilderContext, direction: SortDirection
    ) -> SALoaderBuilderContext:
        pass


class SAQueryFilter(QueryFilter[SALoaderBuilderContext]):
    def apply_filter(
        self, context: SALoaderBuilderContext, reference_value: Optional[Any]
    ) -> SALoaderBuilderContext:
        pass


class SAJoinExtension(QueryExtension[SALoaderBuilderContext]):
    def __init__(self, join_to, sub_query_name: Optional[str] = None):
        super().__init__()
        self._join_to = join_to
        self._sub_query_name = sub_query_name

    def apply_extension(
        self, context: SALoaderBuilderContext
    ) -> SALoaderBuilderContext:
        if self._sub_query_name is None:
            context.main_query = context.main_query.join(self._join_to)
        else:
            q = context.sub_queries[self._sub_query_name]
            context.sub_queries[self._sub_query_name] = q.join(self._join_to)
        return context
