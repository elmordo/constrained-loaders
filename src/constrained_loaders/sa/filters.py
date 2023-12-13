from __future__ import annotations

import functools
from typing import Optional, Any, List, Callable

from constrained_loaders import QueryFilter
from constrained_loaders.sa.context import SALoaderBuilderContext


class SAQueryFilter(QueryFilter[SALoaderBuilderContext]):
    def __init__(
        self,
        clause_factory: Callable[[Any], Any],
        sub_query_name: Optional[str] = None,
        required_extensions: Optional[List[str]] = None,
    ):
        super().__init__(required_extensions)
        self._sub_query_name = sub_query_name
        self._clause_factory = clause_factory

    def apply_filter(
        self, context: SALoaderBuilderContext, reference_value: Optional[Any]
    ) -> SALoaderBuilderContext:
        context.add_filter(
            functools.partial(self._modify_query, reference_value=reference_value)
        )
        return context

    def _modify_query(
        self, context: SALoaderBuilderContext, reference_value: Optional[Any]
    ):
        clause = self._clause_factory(reference_value)
