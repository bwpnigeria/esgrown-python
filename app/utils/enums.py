#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-05-08 18:05:48
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from enum import Enum


class ActionStatus(str, Enum):
    success = "success"
    failed = "failed"


class Gender(str, Enum):
    male = "m"
    female = "f"
    na = "NA"


class AccounType(str, Enum):
    student = "student"
    teacher = "teacher"
    staff = "staff"
    business = "business"
    private = "private"


class CooporateType(str, Enum):
    company = "company"
    school = "school"


class SubscriptionType(str, Enum):
    basic = "basic"
    premium = "premium"


class SubscriptionPlan(str, Enum):
    monthly = "monthly"
    quarterly = "quarterly"
    biannual = "biannual"
    annualy = "annualy"


class SubscriptionMode(str, Enum):
    default = "default"
    scheduled = "scheduled"


class SubscriptionTarget(str, Enum):
    people = "people"
    business = "business"


class FileFormat(str, Enum):
    pdf = ".pdf"
    excel = ".xlsx"
    csv = ".csv"
    json = ".json"
    xml = ".xml"


class WalletStatus(str, Enum):
    enabled = "enabled"
    disabled = "disabled"
    closed = "closed"
