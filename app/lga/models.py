#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2023-10-25 00:54:37
# @Author  : Dahir Muhammad Dahir (dahirmuhammad3@gmail.com)
# @Link    : link
# @Version : 1.0.0


from typing import Any
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.mixins.columns import BaseModelMixin


class State(BaseModelMixin, Base):
    name = Column(String(45), nullable=False, unique=True)


class LocalGovernment(BaseModelMixin, Base):
    name = Column(String(45), nullable=False, unique=True)
    state_id = Column(String(45), ForeignKey("states.uuid"), nullable=False)
    display_name = Column(String(45), nullable=False, unique=True)

    state: Any = relationship("State", lazy="joined", foreign_keys=[state_id])
