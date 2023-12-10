from __future__ import annotations

from typing import Dict

from sqlalchemy import Select


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
