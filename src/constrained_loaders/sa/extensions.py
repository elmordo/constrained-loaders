# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Optional

from constrained_loaders import QueryExtension
from constrained_loaders.sa.context import SALoaderBuilderContext


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
