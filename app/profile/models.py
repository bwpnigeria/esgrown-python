#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2024-08-26 12:14
# @Author  : Nasir Lawal (nasirlawal001@gmail.com)
# @Link    : link
# @Version : 1.0.0

from typing import Any
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
)

from app.mixins.columns import BaseModelMixin
from app.config.database import Base

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

class Individual(BaseModelMixin, Base):
    email = Column(String(100), nullable=False, unique=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    middlename = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(32), nullable=True)
    state_id = Column(String(45), ForeignKey("states.uuid"), nullable=True)
    lga_id = Column(String(45), ForeignKey("localgovernments.uuid"), nullable=True)
    address = Column(String(255), nullable=True)
    date_of_birth = Column(String(45), nullable=False)
    gender = Column(String(16), nullable=False)
    account_type = Column(String(100), nullable=False)
    photo = Column(String(255), nullable=True)

    @declared_attr
    def creator(cls: Any) -> Any:
        return relationship("User", lazy="joined", foreign_keys=[cls.created_by])
    