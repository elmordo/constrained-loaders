# -*- coding: utf-8 -*-
"""
"""

from __future__ import annotations

from sqlalchemy import Select, select as select_, func
from sqlalchemy.orm import Session

from constrained_loaders import Loader, T


class SALoader(Loader):
    def __init__(self, select: Select, session: Session):
        self._select: Select = select
        self._session: Session = session

    def __next__(self) -> T:
        pass

    def __len__(self) -> int:
        s = select_(func.count()).select_from(self._select.subquery())
        return self._session.scalar(s)
