# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from constrained_loaders import LoaderSpec

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)


users_loader_spec = LoaderSpec(
    sortable_fields={},
    default_sort_by=[],
    filterable_fields={},
)
