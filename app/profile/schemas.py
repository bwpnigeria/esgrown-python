#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2024-08-26 13:24
# @Author  : Nasir Lawal (nasirlawal001@gmail.com)
# @Link    : link
# @Version : 1.0.0
from typing import AnyStr, Any
from uuid import UUID
from datetime import date
from app.mixins.schemas import (
    BaseModelIn,
    BaseModelFilter,
    BaseModelMin,
    BaseModelSearch,
    JoinSearch,
    BaseUACSchemaMixin
)
from app.user.schemas import UserAccountIn, UserSchema, UserUpdate, UserUpdateSelf
from app.utils.custom_validators import LowStr
from app.mixins.commons import ListBase, UserMin
from app.lga.schemas import LocalGovernmentMin, StateMin, CountryMin, CountryOut
from app.utils.enums import Gender, AccounType, CooporateType, SubscriptionType, SubscriptionMode, SubscriptionTarget, SubscriptionPlan
from app.user.models import User

from pydantic import (
    BaseModel,
    computed_field,
    Field,
    conint
)

from decimal import Decimal

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


# ====================[ Framework ]====================

class FrameworkCreate(BaseModel):
    name: str
    description: LowStr | None = None


class FrameworkUpdate(BaseModel):
    name: str | None = None
    description: LowStr | None = None


class FrameworkSchema(BaseUACSchemaMixin):
    pass


class FrameworkList(ListBase):
    items: list[FrameworkSchema]


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


# ====================[ Min ]====================

class CorporateMin(BaseModelMin):
    name: str
    address: str | None = None
    account_type: str

    classes: list[ClassSchema] | None = None


class SubscriptionOutMin(BaseModelMin):
    audience: str
    title: str
    description: str
    update_type: SubscriptionType
    mode: SubscriptionMode
    reference: str | None = None
    levels: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    scheduled_date: Any | None = None
    scheduled_time: Any | None = None
    subscription_target: SubscriptionTarget | None = None


class SubscriptionPlanMin(BaseModelMin):
    name: str
    duration: SubscriptionPlan
    price: Decimal

    subscription: SubscriptionOutMin | None = None


class UserSubscriptionOutMin(BaseModelMin):
    start_date: date | None = None
    end_date: date | None = None

    subscription_plan: SubscriptionPlanMin

# ====================[ Individual ]====================

class IndividualIn(BaseModelIn):
    date_of_birth: str
    gender: Gender
    account_type: AccounType
    address: str | None = None
    photo: str | None = None

    country_id: str | None = None
    state_id: str | None = None
    lga_id: str | None = None

    user: UserAccountIn


class IndividualCreate(BaseModel):
    user_id: str
    gender: Gender
    address: str
    account_type: AccounType
    date_of_birth: str
    photo: str | None = None

    user: UserSchema


class IndividualUpdate(BaseModelIn):
    address: str | None = None
    date_of_birth: str | None = None
    gender: Gender | None = None
    account_type: AccounType | None = None
    photo: str | None = None
    profession: str | None = None
    qualification: str | None = None
    institution: str | None = None
    programme: str | None = None
    skills: str | None = None
    employers: list[str] | None = None

    country_id: str | None = None
    state_id: str | None = None
    lga_id: str | None = None

    user: UserUpdate | None = Field(None, exclude=True)


class IndividualUpdateSelf(BaseModelIn):
    address: str | None = None
    date_of_birth: str | None = None
    gender: Gender | None = None
    account_type: AccounType | None = None
    photo: str | None = None
    profession: str | None = None
    qualification: str | None = None
    institution: str | None = None
    programme: str | None = None
    skills: str | None = None
    employers: list[str] | None = None

    country_id: str | None = None
    state_id: str | None = None
    lga_id: str | None = None

    user: UserUpdateSelf | None = Field(None, exclude=True)


class IndividualFilter(BaseModelFilter):
    address: str | None = None
    date_of_birth: str | None = None
    gender: Gender | None = None
    account_type: AccounType | None = None
    photo: str | None = None
    profession: str | None = None
    qualification: str | None = None
    institution: str | None = None
    programme: str | None = None
    skills: str | None = None

    country_id: str | None = None
    state_id: str | None = None
    lga_id: str | None = None


class IndividualSearch(BaseModelSearch):
    @computed_field
    @property
    def search_fields(self) -> list[str]:
        return ["gender", "address", "date_of_birth", "account_type", "profession", "qualification", "institution", "programme", "skills"]

    @computed_field
    @property
    def join_search(self) -> list[JoinSearch]:
        return [
            JoinSearch(model=User, column="firstname", onkey="user_id"),
            JoinSearch(model=User, column="lastname", onkey="user_id"),
            JoinSearch(model=User, column="email", onkey="user_id"),
        ]


class IndividualOut(BaseModelMin):
    address: str | None = None
    date_of_birth: str | None = None
    gender: Gender 
    photo: str | None = None
    account_type: str
    profession: str | None = None
    qualification: str | None = None
    institution: str | None = None
    programme: str | None = None
    skills: str | None = None

    country: CountryMin | None = None
    state: StateMin | None = None
    lga: LocalGovernmentMin | None = None
    employers: list[CorporateMin] | None = None

    subscriptions: list[UserSubscriptionOutMin] | None = None
    user: UserMin


class IndividualMin(BaseModelMin):
    address: str | None = None
    date_of_birth: str | None = None
    gender: Gender
    photo: str | None = None
    account_type: str
    profession: str | None = None
    qualification: str | None = None
    institution: str | None = None
    programme: str | None = None
    skills: str | None = None

    country: CountryMin | None = None
    state: StateMin | None = None
    lga: LocalGovernmentMin | None = None

    user: UserMin


class IndividualList(ListBase):
    items: list[IndividualOut]


# ====================[ Corporate ]====================


class CorporateIn(BaseModelIn):
    name: str
    address: str | None = None
    account_type: CooporateType
    delivery_level: str | None = None
    secondary_contacts: str | None = None
    head: str | None = None
    head_contact: str | None = None

    country_id: str | None = None
    state_id: str | None = None
    lga_id: str | None = None
    photo: str | None = None

    user: UserAccountIn


class CorporateCreate(BaseModel):
    user_id: str
    name: str
    account_type: CooporateType
    address: str | None = None
    delivery_level: str | None = None
    secondary_contacts: str | None = None
    head: str | None = None
    head_contact: str | None = None

    user: UserSchema


class CorporateUpdate(BaseModelIn):
    name: str | None = None
    address: str | None = None
    account_type: CooporateType | None = None
    delivery_level: str | None = None
    secondary_contacts: str | None = None
    head: str | None = None
    head_contact: str | None = None

    country_id: str | None = None
    state_id: str | None = None
    lga_id: str | None = None

    employees: list[str] | None = None
    classes: list[str] | None = None

    user: UserUpdate | None = Field(None, exclude=True)


class CorporateUpdateSelf(BaseModelIn):
    name: str | None = None
    address: str | None = None
    account_type: CooporateType | None = None
    delivery_level: str | None = None
    secondary_contacts: str | None = None
    head: str | None = None
    head_contact: str | None = None

    country_id: str | None = None
    state_id: str | None = None
    lga_id: str | None = None

    employees: list[str] | None = None
    classes: list[str] | None = None

    user: UserUpdateSelf | None = Field(None, exclude=True)


class CorporateFilter(BaseModelFilter):
    name: str | None = None
    address: str | None = None
    account_type: CooporateType | None = None
    delivery_level: str | None = None
    secondary_contacts: str | None = None
    head: str | None = None
    head_contact: str | None = None

    country_id: str | None = None
    state_id: str | None = None
    lga_id: str | None = None


class CorporateSearch(BaseModelSearch):
    @computed_field
    @property
    def search_fields(self) -> list[str]:
        return ["name", "address", "delivery_level", "secondary_contacts", "head", "head_contact", "account_type"]

    @computed_field
    @property
    def join_search(self) -> list[JoinSearch]:
        return [
            JoinSearch(model=User, column="firstname", onkey="user_id"),
            JoinSearch(model=User, column="lastname", onkey="user_id"),
            JoinSearch(model=User, column="email", onkey="user_id"),
        ]


class CorporateOut(BaseModelMin):
    name: str
    address: str | None = None
    account_type: str
    delivery_level: str | None = None
    secondary_contacts: str | None = None
    head: str | None = None
    head_contact: str | None = None

    employees: list[IndividualMin] | None = None
    classes: list[ClassSchema] | None = None
    country: CountryMin | None = None
    state: StateMin | None = None
    lga: LocalGovernmentMin | None = None
    
    subscriptions: list[UserSubscriptionOutMin] | None = None
    user: UserMin


class CorporateList(ListBase):
    items: list[CorporateOut]


# ====================[ Subscription ]====================

class SubscriptionIn(BaseModelIn):
    audience: str
    title: str
    description: str
    update_type: SubscriptionType
    mode: SubscriptionMode
    reference: str | None = None
    levels: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    scheduled_date: str | None = None
    scheduled_time: str | None = None
    subscription_target: SubscriptionTarget | None = None
    subject_id: str | None = None
    framework_id: str | None = None


class SubscriptionUpdate(BaseModelIn):
    audience: str | None = None
    title: str | None = None
    description: str | None = None
    update_type: SubscriptionType | None = None
    mode: SubscriptionMode | None = None
    reference: str | None = None
    # skills: str | None = None
    levels: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    scheduled_date: str | None = None
    scheduled_time: str | None = None
    subscription_target: SubscriptionTarget | None = None

    subjects: str | None = None
    framework: str | None = None


class SubscriptionSearch(BaseModelSearch):
    @computed_field
    @property
    def search_fields(self) -> list[str]:
        return ["audience", "title", "description", "update_type", "mode", "reference"]


class SubscriptionFilter(BaseModelFilter):
    audience: str | None = None
    update_type: SubscriptionType | None = None
    mode: SubscriptionMode | None = None
    scheduled_date: str | None = None
    scheduled_time: str | None = None

    subject_id: str | None = None
    framework_id: str | None = None


class SubscriptionOut(BaseModelMin):
    audience: str
    title: str
    description: str
    update_type: SubscriptionType
    mode: SubscriptionMode
    reference: str | None = None
    levels: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    scheduled_date: Any | None = None
    scheduled_time: Any | None = None
    subscription_target: SubscriptionTarget | None = None

    subjects: SubjectSchema | None = None
    framework: FrameworkSchema | None = None
    plans: list[SubscriptionPlanMin] | None = None


class SubscriptionList(ListBase):
    items: list[SubscriptionOut]


# ====================[ Subscription Plan ]====================

class SubscriptionPlanIn(BaseModelIn):
    name: str
    subscription_id: str
    duration: SubscriptionPlan
    price: Decimal | str


class SubscriptionPlanOut(BaseModelMin):
    name: str
    duration: SubscriptionPlan
    price: Decimal

    subscription: SubscriptionOutMin


class SubscriptionPlanUpdate(BaseModelIn):
    name: str | None = None
    duration: SubscriptionPlan | None = None
    price: Decimal | None = None

    subscription: str | None = None


class SubscriptionPlanFilter(BaseModelFilter):
    name: str | None = None
    duration: SubscriptionPlan | None = None
    price: Decimal | None = None

    # subscription: str | None = None


class SubscriptionPlanList(ListBase):
    items: list[SubscriptionPlanOut]


# ====================[ User Subscription ]====================
class UserSubscriptionIn(BaseModelIn):
    individual_id: str | None = None
    corporate_id: str | None = None
    subscription_plan_id: str
    start_date: date
    end_date: date


class UserSubscriptionUpdate(BaseModelIn):
    start_date: date | None = None
    end_date: date | None = None

    subscription_plan: str | None = None


class UserSubscriptionSearch(BaseModelSearch):
    @computed_field
    @property
    def search_fields(self) -> list[str]:
        return ["start_date", "end_date", "subscription_plan"]
  

class UserSubscriptionFilter(BaseModelFilter):
    start_date: date | None = None
    end_date: date | None = None

    subscription_plan_id: str | None = None


class UserSubscriptionOut(BaseModelMin):
    start_date: date | None = None
    end_date: date | None = None

    individual: IndividualMin | None = None 
    corporate: CorporateMin | None = None 
    subscription_plan: SubscriptionPlanMin


class UserSubscriptionList(ListBase):
    items: list[UserSubscriptionOut]


# ====================[ Discount ]====================

class DiscountIn(BaseModelIn):
    name: str
    percentage: Decimal
    plans: list[str]
    countries: list[str] | None = None
    states: list[str] | None = None
    cities: list[str] | None = None


class UpdateDiscount(BaseModelIn):
    name: str | None = None
    percentage: Decimal | None = None
    used_by_users: list[str] | None = None
    plans: list[str] | None = None
    countries: list[str] | None = None
    states: list[str] | None = None
    cities: list[str] | None = None


class DiscountOut(BaseModelMin):
    name: str
    percentage: Decimal
    plans: list[SubscriptionPlanMin] | None = None
    countries: list[CountryOut] | None = None
    states: list[StateMin] | None = None
    cities: list[LocalGovernmentMin] | None = None


class DiscountList(ListBase):
    items: list[DiscountOut]
