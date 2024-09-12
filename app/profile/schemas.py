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
    BaseUACSchemaMixin
)
from app.user.schemas import UserAccountIn, UserSchema, UserUpdate, UserUpdateSelf
from app.utils.custom_validators import CapStr, UpStr, LowStr
from app.mixins.commons import ListBase, UserMin
from app.lga.schemas import LocalGovernmentMin, StateMin, CountryMin
from app.utils.enums import Gender, AccounType, CooporateType
from app.user.models import User
from typing import Optional, List

from pydantic import (
    BaseModel,
    ConfigDict,
    computed_field,
    Field,
)

# ====================[ Subject ]====================

class SubjectCreate(BaseModel):
    name: str
    description: LowStr | None = None


class SubjectUpdate(BaseModel):
    name: str | None = None
    description: LowStr | None = None


class SubjectSchema(BaseUACSchemaMixin):
    pass


class SubjectList(ListBase):
    items: list[SubjectSchema]


# ====================[ Classes ]====================


class ClassCreate(BaseModel):
    name: str
    description: LowStr | None = None


class ClassUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    subjects: list[str] | None = None


class RemoveClassSubject(BaseModel):
    subjects: list[str]


class ClassSchema(BaseUACSchemaMixin):
    subjects: list[SubjectSchema]


class ClassList(ListBase):
    items: list[ClassSchema]

# ====================[ Individual ]====================


class IndividualIn(BaseModelIn):
    date_of_birth: UpStr 
    gender: Gender 
    account_type: AccounType 
    address: UpStr | None = None
    country_id: str | None = None
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
    photo: str | None = None
    profession: str | None = None
    qualification: str | None = None
    institution: str | None = None
    programme: str | None = None
    skills: str | None = None
    school: str | None = None
    classroom: str | None = None
    subject: str | None = None

    country_id: str | None = None
    state_id: str | None = None
    lga_id: str | None = None

    user: UserUpdate | None = Field(None, exclude=True)


class IndividualUpdateSelf(BaseModelIn):
    address: UpStr | None = None
    date_of_birth: UpStr | None = None
    gender: Gender | None = None
    account_type: AccounType | None = None
    photo: str | None = None
    profession: str | None = None
    qualification: str | None = None
    institution: str | None = None
    programme: str | None = None
    skills: str | None = None
    school: str | None = None
    classroom: str | None = None
    subject: str | None = None

    country_id: str | None = None
    state_id: str | None = None
    lga_id: str | None = None

    user: UserUpdateSelf | None = Field(None, exclude=True)


class IndividualFilter(BaseModelFilter):
    address: UpStr | None = None
    date_of_birth: UpStr | None = None
    gender: Gender | None = None
    account_type: AccounType | None = None
    photo: str | None = None
    profession: str | None = None
    qualification: str | None = None
    institution: str | None = None
    programme: str | None = None
    skills: str | None = None
    school: str | None = None
    classroom: str | None = None
    subject: str | None = None

    country_id: str | None = None
    state_id: str | None = None
    lga_id: str | None = None


class IndividualSearch(BaseModelSearch):
    @computed_field
    @property
    def search_fields(self) -> list[str]:
        return ["gender", "address", "date_of_birth", "account_type"]

    @computed_field
    @property
    def join_search(self) -> list[JoinSearch]:
        return [
            JoinSearch(model=User, column="firstname", onkey="user_id"),
            JoinSearch(model=User, column="lastname", onkey="user_id"),
            JoinSearch(model=User, column="email", onkey="user_id"),
        ]


class IndividualOut(BaseModelMin):
    address: UpStr 
    date_of_birth: UpStr 
    gender: Gender 
    photo: str | None = None
    account_type: str
    profession: str | None = None
    qualification: str | None = None
    institution: str | None = None
    programme: str | None = None
    skills: str | None = None
    school: str | None = None
    classroom: str | None = None
    subject: str | None = None


    country: CountryMin | None = None
    state: StateMin | None = None
    lga: LocalGovernmentMin | None = None

    user: UserMin


class IndividualList(ListBase):
    items: list[IndividualOut]


# ====================[ Corporate ]====================


# class CoporateIn(BaseModelIn):
#     date_of_birth: UpStr
#     gender: Gender
#     account_type: AccounType
#     address: UpStr | None = None
#     country_id: str | None = None
#     state_id: str | None = None
#     lga_id: str | None = None
#     photo: str | None = None
#
#     user: UserAccountIn