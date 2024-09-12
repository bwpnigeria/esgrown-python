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
    ForeignKey, Table,
)

from app.mixins.columns import BaseMixin, BaseModelMixin, BaseUACMixin
from app.config.database import Base
from sqlalchemy.orm import relationship

# Many to many associations
subject_class = Table(
    'subject_class', Base.metadata,
    Column('subject_id', String(length=50), ForeignKey('subjects.uuid')),
    Column('class_id', String(length=50), ForeignKey('classes.uuid')),
)
class_corporate = Table(
    'class_corporate', Base.metadata,
    Column('class_id', String(length=50), ForeignKey('classes.uuid')),
    Column('corporate_id', String(length=50), ForeignKey('corporates.uuid')),
)

individual_corporate = Table(
    'individual_corporate', Base.metadata,
    Column('individual_id', String(length=50), ForeignKey('individuals.uuid')),
    Column('corporate_id', String(length=50), ForeignKey('corporates.uuid')),
)


class Individual(BaseMixin, Base):
    user_id = Column(String(45), ForeignKey("users.uuid"), nullable=False)
    country_id = Column(String(45), ForeignKey("countries.uuid"), nullable=True)
    state_id = Column(String(45), ForeignKey("states.uuid"), nullable=True)
    lga_id = Column(String(45), ForeignKey("localgovernments.uuid"), nullable=True)

    address = Column(String(255), nullable=True)
    date_of_birth = Column(String(45), nullable=False)
    gender = Column(String(16), nullable=False)
    account_type = Column(String(100), nullable=False)
    photo = Column(String(255), nullable=True)
    profession = Column(String(255), nullable=True)
    institution = Column(String(255), nullable=True)
    qualification = Column(String(255), nullable=True)
    programme = Column(String(255), nullable=True)
    skills = Column(String(255), nullable=True)
    school = Column(String(255), nullable=True)
    classroom = Column(String(255), nullable=True)
    subject = Column(String(255), nullable=True)

    user: Any = relationship("User", lazy="joined", foreign_keys=[user_id])
    country: Any = relationship("Country", lazy="joined", foreign_keys=[country_id])
    state: Any = relationship("State", lazy="joined", foreign_keys=[state_id])
    lga: Any = relationship("LocalGovernment", lazy="joined", foreign_keys=[lga_id])
    employers: Any = relationship("Corporate", secondary=individual_corporate, back_populates="employees", uselist=True)


class Corporate(BaseMixin, Base):
    user_id = Column(String(45), ForeignKey("users.uuid"), nullable=False)
    country_id = Column(String(45), ForeignKey("countries.uuid"), nullable=True)
    state_id = Column(String(45), ForeignKey("states.uuid"), nullable=True)
    lga_id = Column(String(45), ForeignKey("localgovernments.uuid"), nullable=True)

    name = Column(String(255), nullable=False)
    account_type = Column(String(100), nullable=False)
    delivery_level = Column(String(255), nullable=True)
    secondary_contacts = Column(String(255), nullable=True)
    head = Column(String(255), nullable=True)
    head_contact = Column(String(255), nullable=True, unique=True)

    employees: Any = relationship("Individual", secondary=individual_corporate, back_populates='employers', uselist=True)
    classes: Any = relationship('Class', secondary=class_corporate, uselist=True)
    user: Any = relationship("User", lazy="joined", foreign_keys=[user_id])
    country: Any = relationship("Country", lazy="joined", foreign_keys=[country_id])
    state: Any = relationship("State", lazy="joined", foreign_keys=[state_id])
    lga: Any = relationship("LocalGovernment", lazy="joined", foreign_keys=[lga_id])


class Class(BaseMixin, Base):
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    subjects: Any = relationship("Subject", secondary=subject_class)


class Subject(BaseMixin, Base):
    name = Column(String(255), nullable=False)
    description = Column(String(255))