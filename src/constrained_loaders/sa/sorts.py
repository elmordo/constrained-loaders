from __future__ import annotations

from constrained_loaders import QuerySort, SortDirection
from constrained_loaders.sa.context import SALoaderBuilderContext


class SAQuerySort(QuerySort[SALoaderBuilderContext]):
    def apply_sorting(
        self, context: SALoaderBuilderContext, direction: SortDirection
    ) -> SALoaderBuilderContext:
        pass
