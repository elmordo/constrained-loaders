# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Generic, Optional, Any, Callable

from sqlalchemy import Select
from sqlalchemy.orm import Session

from constrained_loaders import (
    LoaderBuilderBase,
    T,
    LoaderSpec,
    QuerySort,
    SortDirection,
    QueryFilter,
)
from .loader import SALoader


class SASimpleLoaderBuilder(LoaderBuilderBase[T, Select], Generic[T]):
    """This loader is suitable for most use cases. But if you need more complex queries (with sub-queries, etc, use
    SAComplexLoaderBuilder instead)
    """

    def __init__(self, spec: LoaderSpec[Select], bare_query: Select, session: Session):
        super().__init__(spec, bare_query)
        self._session: Session = session

    def set_offset(self, offset: int) -> None:
        self._query = self._query.offset(offset)

    def set_limit(self, limit: int) -> None:
        self._query = self._query.limit(limit)

    def build(self) -> SALoader[T]:
        return SALoader(self._query, self._session)


class SASimpleQuerySort(QuerySort[Select]):
    def __init__(self, expr):
        super().__init__()
        self._expr = expr

    def apply_sorting(self, query: Select, direction: SortDirection) -> Select:
        if direction is SortDirection.UNSPECIFIED:
            order_by = self._expr
        elif direction is SortDirection.ASC:
            order_by = self._expr.asc()
        elif direction is SortDirection.DESC:
            order_by = self._expr.desc()
        else:
            raise ValueError(f"Unknown sort direction '{direction}'")
        return query.order_by(order_by)


class SASimpleQueryFilter(QueryFilter[Select]):
    def __init__(self, expr, filter_factory: Callable[[Any, Any], Any]):
        super().__init__()
        self._expr = expr
        self._filter_factory = filter_factory

    def apply_filter(self, query: Select, reference_value: Optional[Any]) -> Select:
        return query.where(self._filter_factory(self._expr, reference_value))
