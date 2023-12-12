from __future__ import annotations

from typing import Dict, Protocol, List

from sqlalchemy import Select


class SALoaderBuilderContext:
    def __init__(self, initial_select: Select):
        self.main_query = initial_select
        self.sub_queries: Dict[str, Select] = {}
        self._filters: List[SABuilderContextApplicator] = []
        self._sorts: List[SABuilderContextApplicator] = []
        self._extensions: List[SABuilderContextApplicator] = []

    def add_filter(self, filter_: SABuilderContextApplicator):
        self._filters.append(filter_)

    def add_sort(self, sort: SABuilderContextApplicator):
        self._sorts.append(sort)

    def add_extension(self, extension: SABuilderContextApplicator):
        self._extensions.append(extension)

    def build_select(self) -> Select:
        self._apply_extensions()
        self._apply_filters()
        self._apply_sorts()
        return self.main_query

    def _apply_extensions(self):
        for e in self._extensions:
            e(self)

    def _apply_filters(self):
        for f in self._filters:
            f(self)

    def _apply_sorts(self):
        for s in self._sorts:
            s(self)


class SABuilderContextApplicator(Protocol):
    def __call__(self, context: SALoaderBuilderContext):
        pass
