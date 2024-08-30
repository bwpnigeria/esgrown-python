#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-05-06 14:32:47
# @Author  : Dahir Muhammad Dahir
# @Description : Based on bills fastapi template


from enum import Enum
from app.utils.enums import ActionStatus
from datetime import datetime, date as dt_date
from typing import Any, Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class BaseSchemaMixin(BaseModel):
    id: int
    uuid: str
    date: dt_date
    created_at: datetime
    last_modified: datetime

    model_config = ConfigDict(from_attributes=True)


class BaseSchemaMixinMin(BaseModel):
    id: int
    uuid: str
    date: dt_date
    created_at: datetime
    last_modified: datetime

    model_config = ConfigDict(from_attributes=True)


class BaseUACSchemaMixin(BaseSchemaMixin):
    name: str
    description: Optional[str]


class UserMin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    firstname: str
    lastname: str
    middlename: str | None = ""
    phone: str | None = ""


class Processor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    firstname: str
    lastname: str
    middlename: str | None = ""


class BaseModelOut(BaseSchemaMixin):
    created_by: str

    creator: UserMin


class BaseModelMin(BaseSchemaMixinMin):
    pass


class BaseModelIn(BaseModel):
    model_config = ConfigDict(str_max_length=6144)


class BaseModelPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OrderType(str, Enum):
    asc = "asc"
    desc = "desc"


class BaseModelFilter(BaseModelIn):
    model_config = ConfigDict(str_to_upper=False)
    skip: int = 0
    limit: int = 10
    order: OrderType = OrderType.asc


class BaseModelSearch(BaseModelIn):
    model_config = ConfigDict(str_to_upper=False)
    search: str
    skip: int = 0
    limit: int = 10
    order: OrderType = OrderType.asc


class JoinSearch(BaseModel):
    model: Any
    column: str
    onkey: str


class BaseModelCreate(BaseModel):
    created_by: str


class Status(BaseModel):
    status: ActionStatus
