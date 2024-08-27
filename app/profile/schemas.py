#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2024-08-26 13:24
# @Author  : Nasir Lawal (nasirlawal001@gmail.com)
# @Link    : link
# @Version : 1.0.0

from app.mixins.schemas import (
    BaseModelIn,
    BaseModelCreate,
    BaseModelFilter,
    BaseModelMin,
    BaseModelSearch,
    BaseModelOut,
    JoinSearch,
)
from app.user.models import User
from app.user.schemas import UserIn, UserUpdate, UserUpdateSelf
from app.utils.custom_validators import CapStr, UpStr
from app.mixins.commons import ListBase, UserMin, UserPublic
from app.lga.schemas import LocalGovernmentMin, StateMin
from app.utils.enums import Gender, AccounType
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
    ValidationInfo,
    computed_field,
    Field,
    field_validator,
)


class IndividualIn(BaseModelIn):
    email: str
    firstname: CapStr
    lastname: CapStr
    phone: str
    address: UpStr | None = None
    date_of_birth: UpStr | None = None
    gender: Gender | None = None
    account_type: AccounType 
    password: str


class IndividualCreate(BaseModel):
    email: str
    phone: str
    firstname: CapStr
    lastname: CapStr
    address: UpStr
    gender: Gender
    account_type: AccounType  
    date_of_birth: UpStr
    password_hash: str


class IndividualUpdate(BaseModelIn):
    email: str | None = None
    firstname: CapStr | None = None
    lastname: CapStr | None = None
    phone: str | None = None
    address: UpStr | None = None
    date_of_birth: UpStr | None = None
    gender: Gender | None = None
    nationality: CapStr | None = None
    state_id: str | None = None
    lga_id: str | None = None
    photo: str | None = None


class IndividualFilter(BaseModelFilter):
    email: str | None = None
    firstname: CapStr | None = None
    lastname: CapStr | None = None
    phone: str | None = None
    address: UpStr | None = None
    date_of_birth: UpStr | None = None
    gender: Gender | None = None
    nationality: CapStr | None = None
    state_id: str | None = None
    lga_id: str | None = None
    photo: str | None = None


class IndividualSearch(BaseModelSearch):
    @computed_field
    @property
    def search_fields(self) -> list[str]:
        return ["firstname", "lastname", "email", "phone"]


class IndividualOut(BaseModelMin):
    email: str
    firstname: CapStr
    lastname: CapStr
    nationality: CapStr | None = None
    address: UpStr 
    date_of_birth: UpStr 
    gender: Gender 
    photo: str | None = None
    account_type: str
    state: StateMin | None = None
    lga: LocalGovernmentMin | None = None



class IndividualList(ListBase):
    items: list[IndividualOut]