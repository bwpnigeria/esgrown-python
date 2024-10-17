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
    Integer,
    ForeignKey,
    Table,
    Time,
    Date,
    Numeric,
    Boolean
)
from app.mixins.columns import BaseMixin
from app.config.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

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
    Column('individual_id', String(length=50), ForeignKey('individuals.uuid'), nullable=True),
    Column('corporate_id', String(length=50), ForeignKey('corporates.uuid'), nullable=True),
)


class Individual(BaseMixin, Base):
    user_id = Column(String(45), ForeignKey("users.uuid"), nullable=False)
    country_id = Column(String(45), ForeignKey("countries.uuid"), nullable=True)
    state_id = Column(String(45), ForeignKey("states.uuid"), nullable=True)
    lga_id = Column(String(45), ForeignKey("localgovernments.uuid"), nullable=True)

    address = Column(String(255), nullable=True)
    date_of_birth = Column(String(45), nullable=True)
    gender = Column(String(16), nullable=False)
    account_type = Column(String(100), nullable=False)
    photo = Column(String(255), nullable=True)
    profession = Column(String(255), nullable=True)
    institution = Column(String(255), nullable=True)
    qualification = Column(String(255), nullable=True)
    programme = Column(String(255), nullable=True)
    skills = Column(String(255), nullable=True)

    user: Any = relationship("User", lazy="joined", foreign_keys=[user_id])
    country: Any = relationship("Country", lazy="joined", foreign_keys=[country_id])
    state: Any = relationship("State", lazy="joined", foreign_keys=[state_id])
    lga: Any = relationship("LocalGovernment", lazy="joined", foreign_keys=[lga_id])
    employers: Any = relationship("Corporate", secondary=individual_corporate, back_populates="employees", uselist=True)

    subscriptions = relationship("UserSubscription", back_populates="individual")


class Corporate(BaseMixin, Base):
    user_id = Column(String(45), ForeignKey("users.uuid"), nullable=False)
    country_id = Column(String(45), ForeignKey("countries.uuid"), nullable=True)
    state_id = Column(String(45), ForeignKey("states.uuid"), nullable=True)
    lga_id = Column(String(45), ForeignKey("localgovernments.uuid"), nullable=True)

    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    account_type = Column(String(100), nullable=False)
    delivery_level = Column(String(255), nullable=True)
    secondary_contacts = Column(String(255), nullable=True)
    head = Column(String(255), nullable=True)
    head_contact = Column(String(255), nullable=True)

    employees: Any = relationship("Individual", secondary=individual_corporate, back_populates='employers', uselist=True)
    classes: Any = relationship('Class', secondary=class_corporate, uselist=True)
    user: Any = relationship("User", lazy="joined", foreign_keys=[user_id])
    country: Any = relationship("Country", lazy="joined", foreign_keys=[country_id])
    state: Any = relationship("State", lazy="joined", foreign_keys=[state_id])
    lga: Any = relationship("LocalGovernment", lazy="joined", foreign_keys=[lga_id])

    subscriptions = relationship("UserSubscription", back_populates="corporate")


class Class(BaseMixin, Base):
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    subjects: Any = relationship("Subject", secondary=subject_class)


class Subject(BaseMixin, Base):
    name = Column(String(255), nullable=False)
    description = Column(String(255))


class Framework(BaseMixin, Base):
    name = Column(String(255), nullable=False)
    description = Column(String(255))


class Subscription(BaseMixin, Base):
    subject_id = Column(String(45), ForeignKey("subjects.uuid"), nullable=True)
    framework_id = Column(String(45), ForeignKey("frameworks.uuid"), nullable=True)
    audience = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    update_type = Column(String(255), nullable=False)
    mode = Column(String(255), nullable=False)
    reference = Column(String(2048), nullable=True)
    levels = Column(String(255), nullable=True)
    skills = Column(String(1000), nullable=True)
    image_url = Column(String(2048), nullable=True)
    video_url = Column(String(2048), nullable=True)
    scheduled_date = Column(Date, nullable=True)
    scheduled_time = Column(Time, nullable=True)
    subscription_target = Column(String(255), nullable=True)

    plans = relationship("SubscriptionPlan", back_populates="subscription")

    subjects: Any = relationship("Subject", lazy="joined", foreign_keys=[subject_id])
    framework: Any = relationship("Framework", lazy="joined", foreign_keys=[framework_id])


class SubscriptionPlan(BaseMixin, Base):    
    subscription_id = Column(String(45), ForeignKey("subscriptions.uuid"), nullable=False)
    name = Column(String(255), nullable=False)
    duration = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    subscription = relationship("Subscription", back_populates="plans")


class UserSubscription(BaseMixin, Base):
    individual_id = Column(String, ForeignKey("individuals.uuid"), nullable=True)
    corporate_id = Column(String, ForeignKey("corporates.uuid"), nullable=True)
    subscription_plan_id = Column(String, ForeignKey("subscriptionplans.uuid"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    individual: Any = relationship("Individual", lazy="joined")
    corporate: Any = relationship("Corporate", lazy="joined")
    subscription_plan: Any = relationship("SubscriptionPlan", lazy="joined")
