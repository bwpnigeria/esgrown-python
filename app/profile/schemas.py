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
from app.user.schemas import UserAccountIn, UserSchema, UserUpdate, UserUpdateSelf
from app.utils.custom_validators import CapStr, UpStr
from app.mixins.commons import ListBase, UserMin
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
    date_of_birth: UpStr 
    gender: Gender 
    account_type: AccounType 
    address: UpStr | None = None
    state_id: str | None = None
    lga_id: str | None = None
    photo: str | None = None

    user: UserAccountIn


class IndividualCreate(BaseModel):
    user_id: str
    gender: Gender
    address: UpStr
    account_type: AccounType
    date_of_birth: UpStr
    photo: str | None = None

    user: UserSchema


class IndividualUpdate(BaseModelIn):
    address: UpStr | None = None
    date_of_birth: UpStr | None = None
    gender: Gender | None = None
    account_type: AccounType | None = None
    state_id: str | None = None
    lga_id: str | None = None
    photo: str | None = None

    user: UserUpdate | None = Field(None, exclude=True)


class IndividualUpdateSelf(BaseModelIn):
    address: UpStr | None = None
    date_of_birth: UpStr | None = None
    gender: Gender | None = None
    account_type: AccounType | None = None
    photo: str | None = None

    user: UserUpdateSelf | None = Field(None, exclude=True)


class IndividualFilter(BaseModelFilter):
    address: UpStr | None = None
    date_of_birth: UpStr | None = None
    gender: Gender | None = None
    account_type: AccounType | None = None
    state_id: str | None = None
    lga_id: str | None = None
    photo: str | None = None


class IndividualSearch(BaseModelSearch):
    @computed_field
    @property
    def search_fields(self) -> list[str]:
        return ["gender", "address", "date_of_birth", "account_type"]


class IndividualOut(BaseModelMin):
    address: UpStr 
    date_of_birth: UpStr 
    gender: Gender 
    photo: str | None = None
    account_type: str
    state: StateMin | None = None
    lga: LocalGovernmentMin | None = None

    user: UserMin


class IndividualList(ListBase):
    items: list[IndividualOut]
