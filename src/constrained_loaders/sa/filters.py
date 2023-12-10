from __future__ import annotations

from typing import Optional, Any

from constrained_loaders import QueryFilter
from constrained_loaders.sa.context import SALoaderBuilderContext


class SAQueryFilter(QueryFilter[SALoaderBuilderContext]):
    def apply_filter(
        self, context: SALoaderBuilderContext, reference_value: Optional[Any]
    ) -> SALoaderBuilderContext:
        pass
