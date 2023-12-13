# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from typing import Iterable, Callable, Sequence, Self

from constrained_loaders.abstraction import Loader, T


class DummyLoader(Loader[T]):
    """The dummy loader returns empty set of items"""

    def __iter__(self) -> Iterable[T]:
        return []

    def __len__(self) -> int:
        return 0


class FactoryLoader(Loader[T]):
    """Return items provided by the `item_sequence_factory` callback.

    This loader can be used for testing or as wrapper.
    """

    def __init__(self, item_sequence_factory: Callable[[], Sequence[T]]):
        self._item_sequence_factory = item_sequence_factory
        self._prepared_sequence = None

    def __iter__(self) -> Iterable[T]:
        s = self._prepare_sequence()
        self._prepared_sequence = None
        return s

    def __len__(self) -> int:
        return len(self._prepared_sequence())

    @classmethod
    def from_iterable(cls, item_sequence: Iterable[T]) -> Self:
        """Create new instance from an iterable of items. The iterable is consumed when creating items sequence used in
        the loader instance"""
        items = list(item_sequence)
        return cls(lambda: items)

    def _prepare_sequence(self) -> Sequence[T]:
        """Prepare the sequence of items and store it into instance state. If sequence is prepared, only returns the
        sequence."""
        if self._prepared_sequence is None:
            self._prepared_sequence = self._item_sequence_factory()
        return self._prepared_sequence
