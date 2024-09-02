#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2023-10-25 00:58:26
# @Author  : Dahir Muhammad Dahir (dahirmuhammad3@gmail.com)
# @Link    : link
# @Version : 1.0.0


from pydantic import BaseModel, ConfigDict
from app.mixins.commons import ListBase
from app.mixins.schemas import (
    BaseModelIn,
    BaseModelCreate,
    BaseModelFilter,
    BaseModelOut,
)

from app.utils.custom_validators import UpStr


# ======================[ Country ]======================

class CountryIn(BaseModelIn):
    name: UpStr


class CountryCreate(BaseModelCreate):
    name: UpStr


class CountryUpdate(BaseModelIn):
    name: UpStr | None = None


class CountryFilter(BaseModelFilter):
    name: UpStr | None = None


class CountryOut(BaseModelOut):
    name: UpStr


class CountryMin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: str
    name: UpStr


class CountryList(ListBase):
    items: list[CountryOut]


# ======================[ State ]======================


class StateIn(BaseModelIn):
    name: UpStr
    country_id: str


class StateCreate(BaseModelCreate):
    name: UpStr
    country_id: str


class StateUpdate(BaseModelIn):
    name: UpStr | None = None
    country_id: str | None = None


class StateFilter(BaseModelFilter):
    name: UpStr | None = None
    country_id: str | None = None


class StateOut(BaseModelOut):
    name: UpStr
    country_id: str

    country: CountryMin


class StateMin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: str
    name: UpStr
    country_id: str

    country: CountryMin


class StateList(ListBase):
    items: list[StateOut]


# ======================[ Local Government ]======================


class LocalGovernmentIn(BaseModelIn):
    name: UpStr
    state_id: str
    display_name: UpStr


class LocalGovernmentCreate(BaseModelCreate):
    name: UpStr
    state_id: str
    display_name: UpStr


class LocalGovernmentUpdate(BaseModelIn):
    name: UpStr | None = None
    state_id: str | None = None
    display_name: UpStr | None = None


class LocalGovernmentFilter(BaseModelFilter):
    name: UpStr | None = None
    state_id: str | None = None
    display_name: UpStr | None = None


class LocalGovernmentOut(BaseModelOut):
    name: UpStr
    state_id: str
    display_name: UpStr

    state: StateMin


class LocalGovernmentMin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: str
    name: UpStr
    state_id: str
    display_name: UpStr

    state: StateMin


class LocalGovernmentList(ListBase):
    items: list[LocalGovernmentOut]
