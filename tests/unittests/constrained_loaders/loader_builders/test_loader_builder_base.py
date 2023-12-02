# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import List, Optional, Any

import pytest

from constrained_loaders.abstraction import (
    Loader,
    T,
    LoaderSpec,
    QuerySort,
    SortDirection,
    QueryFilter,
    LoaderExtension,
)
from constrained_loaders.loader_builders import LoaderBuilderBase


@pytest.fixture()
def spec() -> LoaderSpec:
    return LoaderSpec(
        sortable_fields={
            "id": SampleSort("id"),
            "name": SampleSort("name", ["ext1"]),
        },
        default_sort_by=[],
        filterable_fields={
            "id": {
                "eq": SampleFilter("id_eq"),
            },
            "address": {
                "like": SampleFilter("address_like", "ext2"),
            },
        },
        extensions={
            "ext1": SampleExtension("ext1"),
            "ext2": SampleExtension("ext2", ["ext3"]),
            "ext3": SampleExtension("ext3"),
        },
    )


class SampleSort(QuerySort[List]):
    def __init__(self, name, extensions=None):
        super().__init__(extensions)
        self.name = name

    def apply_sorting(self, query: List, direction: SortDirection) -> List:
        query.append(("sort", self.name))
        return query


class SampleFilter(QueryFilter[List]):
    def __init__(self, name, extensions=None):
        super().__init__(extensions)
        self.name = name

    def apply_filter(self, query: List, reference_value: Optional[Any]) -> List:
        query.append(("filter", (self.name, reference_value)))
        return query


class SampleExtension(LoaderExtension[List]):
    def __init__(self, name, requirements=None):
        super().__init__(requirements)
        self.name = name

    def apply_extension(self, query: List) -> List:
        query.append(("extension", self.name))
        return query


class SampleLoaderBuilder(LoaderBuilderBase):
    def set_offset(self, offset: int) -> None:
        raise NotImplementedError()

    def set_limit(self, limit: int) -> None:
        raise NotImplementedError()

    def build(self) -> Loader[T]:
        raise NotImplementedError()
