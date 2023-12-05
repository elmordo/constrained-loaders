# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import List, Optional, Any

import pytest

from constrained_loaders import (
    Loader,
    T,
    LoaderSpec,
    QuerySort,
    SortDirection,
    QueryFilter,
    QueryExtension,
    SortNotFound,
    FilterNotFound,
    LoaderBuilderBase,
    ExtensionNotFound,
)


@pytest.mark.parametrize(
    "field, direction, expected_result",
    [
        (
            "id",
            SortDirection.ASC,
            [("sort", ("id", SortDirection.ASC))],
        ),
        (
            "name",
            SortDirection.ASC,
            [("extension", "ext1"), ("sort", ("name", SortDirection.ASC))],
        ),
    ],
)
def test_add_sort(builder, query, field, direction: SortDirection, expected_result):
    assert builder.is_any_sort_applied is False
    builder.add_sort(field, direction)
    assert query == expected_result
    assert builder.is_any_sort_applied is True


@pytest.mark.parametrize(
    "field, operator, reference_value, expected_result",
    [
        (
            "id",
            "eq",
            12,
            [("filter", ("id_eq", 12))],
        ),
        (
            "address",
            "like",
            "some town 666",
            [
                ("extension", "ext3"),
                ("extension", "ext2"),
                ("filter", ("address_like", "some town 666")),
            ],
        ),
    ],
)
def test_add_filter(builder, query, field, operator, reference_value, expected_result):
    builder.add_filter(field, operator, reference_value)
    assert query == expected_result


@pytest.mark.parametrize(
    "extension, expected_result",
    [
        ("ext1", [("extension", "ext1")]),
        (
            "ext2",
            [
                ("extension", "ext3"),
                ("extension", "ext2"),
            ],
        ),
    ],
)
def test_add_extension(builder, query, extension, expected_result):
    builder.apply_extension(extension)
    assert query == expected_result


def test_add_invalid_sort(builder):
    assert builder.is_any_sort_applied is False
    with pytest.raises(SortNotFound):
        builder.add_sort("foo", SortDirection.ASC)
    assert builder.is_any_sort_applied is False


@pytest.mark.parametrize(
    "field, operator",
    [
        ["foo", "bar"],
        ["id", "bar"],
    ],
)
def test_add_invalid_filter(builder, field, operator):
    with pytest.raises(FilterNotFound):
        builder.add_filter(field, operator, 1)


def test_add_invalid_extension(builder):
    with pytest.raises(ExtensionNotFound):
        builder.apply_extension("foo")


@pytest.fixture()
def builder(spec, query) -> SampleLoaderBuilder:
    return SampleLoaderBuilder(spec, query)


@pytest.fixture()
def query() -> List:
    return []


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
                "like": SampleFilter("address_like", ["ext2"]),
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

    def apply_sorting(self, context: List, direction: SortDirection) -> List:
        context.append(("sort", (self.name, direction)))
        return context


class SampleFilter(QueryFilter[List]):
    def __init__(self, name, extensions=None):
        super().__init__(extensions)
        self.name = name

    def apply_filter(self, context: List, reference_value: Optional[Any]) -> List:
        context.append(("filter", (self.name, reference_value)))
        return context


class SampleExtension(QueryExtension[List]):
    def __init__(self, name, requirements=None):
        super().__init__(requirements)
        self.name = name

    def apply_extension(self, context: List) -> List:
        context.append(("extension", self.name))
        return context


class SampleLoaderBuilder(LoaderBuilderBase):
    def set_offset(self, offset: int) -> None:
        raise NotImplementedError()

    def set_limit(self, limit: int) -> None:
        raise NotImplementedError()

    def build(self) -> Loader[T]:
        raise NotImplementedError()
