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
    ForeignKey, Table, String
)

from app.mixins.columns import BaseMixin, BaseModelMixin
from app.config.database import Base
from sqlalchemy.orm import relationship

# Many to many associations
# subject_class = Table(
#     Column('subjects_id', String(length=50), ForeignKey('subjects.uuid')),
#     Column('class_id', String(length=50), ForeignKey('classes.uuid')),
# )


class Individual(BaseMixin, Base):
    user_id = Column(String(45), ForeignKey("users.uuid"), nullable=False)
    country_id = Column(String(45), ForeignKey("countries.uuid"), nullable=True)
    state_id = Column(String(45), ForeignKey("states.uuid"), nullable=True)
    lga_id = Column(String(45), ForeignKey("localgovernments.uuid"), nullable=True)
    school_id = Column(String(45), ForeignKey("schools.uuid"), nullable=True)
    subject_id = Column(String(45), ForeignKey("subjects.uuid"), nullable=True)

    address = Column(String(255), nullable=True)
    date_of_birth = Column(String(45), nullable=False)
    gender = Column(String(16), nullable=False)
    account_type = Column(String(100), nullable=False)
    photo = Column(String(255), nullable=True)
    profession = Column(String(255), nullable=True)
    qualification = Column(String(255), nullable=True)
    institution = Column(String(255), nullable=True)
    programme = Column(String(255), nullable=True)
    skills = Column(String(255), nullable=True)

    user: Any = relationship("User", lazy="joined", foreign_keys=[user_id])
    country: Any = relationship("Country", lazy="joined", foreign_keys=[country_id])
    state: Any = relationship("State", lazy="joined", foreign_keys=[state_id])
    lga: Any = relationship("LocalGovernment", lazy="joined", foreign_keys=[lga_id])
    school: Any = relationship("School", lazy="joined", foreign_keys=[school_id])
    subject: Any = relationship("Subject", lazy="joined", foreign_keys=[subject_id])


class School(BaseMixin, Base):
    user_id = Column(String(45), ForeignKey("users.uuid"), nullable=False)
    name = Column(String(255), nullable=False)
    account_type = Column(String(100), nullable=False)

    user: Any = relationship("User", lazy="joined", foreign_keys=[user_id])


# class Class(BaseMixin, Base):


class Subject(BaseModelMixin, Base):
    name = Column(String(255), nullable=False, unique=True)
    school_id = Column(String(45), ForeignKey("schools.uuid"), nullable=False)

    school = relationship("School", lazy="joined", foreign_keys=[school_id])