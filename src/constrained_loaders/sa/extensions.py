# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Optional, Iterable

from constrained_loaders import QueryExtension
from constrained_loaders.sa.context import SALoaderBuilderContext


class SAJoinExtension(QueryExtension[SALoaderBuilderContext]):
    def __init__(
        self,
        join_to,
        sub_query_name: Optional[str] = None,
        on_clause=None,
        required_extensions: Optional[Iterable[str]] = None,
    ):
        super().__init__(required_extensions)
        self._on_clause = on_clause
        self._join_to = join_to
        self._sub_query_name = sub_query_name

    def __call__(self, context: SALoaderBuilderContext) -> None:
        if self._sub_query_name is None:
            context.main_query = context.main_query.join(self._join_to, self._on_clause)
        else:
            sq = self._sub_query_name
            context.sub_queries[sq] = context.sub_queries[sq].join(
                self._join_to, self._on_clause
            )

    def apply_extension(
        self, context: SALoaderBuilderContext
    ) -> SALoaderBuilderContext:
        context.add_extension(self)
        return context
