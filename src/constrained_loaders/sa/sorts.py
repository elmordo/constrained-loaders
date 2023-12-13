from __future__ import annotations

import functools
from typing import Iterable, Optional

from constrained_loaders import QuerySort, SortDirection
from constrained_loaders.sa.context import SALoaderBuilderContext


class SAQuerySort(QuerySort[SALoaderBuilderContext]):
    def __init__(
        self,
        expr,
        sub_query_name: Optional[str] = None,
        required_extensions: Optional[Iterable[str]] = None,
    ):
        super().__init__(required_extensions)
        self._expr = expr
        self._sub_query_name = sub_query_name

    def apply_sorting(
        self, context: SALoaderBuilderContext, direction: SortDirection
    ) -> SALoaderBuilderContext:
        context.add_sort(functools.partial(self._modify_query, direction=direction))
        return context

    def _modify_query(
        self, context: SALoaderBuilderContext, direction: SortDirection
    ) -> None:
        if direction is SortDirection.ASC:
            o = self._expr.asc()
        elif direction is SortDirection.DESC:
            o = self._expr.desc()
        elif direction is SortDirection.UNSPECIFIED:
            o = self._expr
        else:
            raise ValueError(f"Invalid sort direction: {direction}")

        if self._sub_query_name is None:
            context.main_query = context.main_query.order_by(o)
        else:
            context.sub_queries[self._sub_query_name] = context.sub_queries[
                self._sub_query_name
            ].order_by(o)
