#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-05-24 00:40:54
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from app.utils.custom_validators import MoneyOut, UpStr
from enum import Enum
from typing import Any


from app.mixins.schemas import BaseModelPublic, BaseSchemaMixin, UserMin
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from datetime import date


class Gender(str, Enum):
    male = "m"
    female = "f"
    na = "na"


class WalletStatus(str, Enum):
    enabled = "enabled"
    disabled = "disabled"
    closed = "closed"


class WalletTxnType(str, Enum):
    credit = "credit"
    debit = "debit"


class WalletType(str, Enum):
    seller = "seller"
    dealer = "dealer"
    passenger = "passenger"


class PaymentProviders(str, Enum):
    flutterwave = "FLUTTERWAVE"
    paystack = "PAYSTACK"
    moniepoint = "MONIEPOINT"


class PaymentInterestType(str, Enum):
    exclusive = "exclusive"
    inclusive = "inclusive"


class PaymentAccountStatus(str, Enum):
    activated = "activated"
    deactivated = "deactivated"
    blacklisted = "blacklisted"


class PaymentTxnStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class TaxPaymentStatus(str, Enum):
    paid = "paid"
    not_paid = "not_paid"


class PaymentStatus(str, Enum):
    paid = "paid"
    not_paid = "not_paid"
    not_activated = "not_activated"


class ApplicationStatus(str, Enum):
    started = "started"
    made_payment = "made_payment"
    filled_bio_data = "filled_bio_data"
    completed = "completed"
    admitted = "admitted"
    rejected = "rejected"
    accepted_admission = "accepted_admission"


class AdmissionStatus(str, Enum):
    admitted = "admitted"
    rejected = "rejected"


class CurrencyType(str, Enum):
    naira = "NGN"
    dollar = "USD"
    euro = "EUR"
    pound = "GBP"


class EnrollmentStatus(str, Enum):
    enrolled = "enrolled"
    not_enrolled = "not_enrolled"


class CardStatus(str, Enum):
    not_activated = "not_activated"
    activated = "activated"
    deactivated = "deactivated"
    blocked = "blocked"


class BusinessStatus(str, Enum):
    active = "active"
    disabled = "disabled"
    closed = "closed"
    blacklisted = "blacklisted"


class BusinessPaymentComponentStatus(str, Enum):
    active = "active"
    disabled = "disabled"


class NINImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nin: str = Field(..., max_length=16)
    image: str = Field(..., max_length=160)


class UserOut(BaseSchemaMixin):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    firstname: UpStr
    lastname: UpStr
    middlename: UpStr | None = ""
    is_active: bool
    is_system_user: bool


class VehicleQROut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    qr_file: str


class DateRange(BaseModel):
    column_name: str = "date"
    from_date: date
    to_date: date


class ListBase(BaseModel):
    count: int
    sum: MoneyOut | None = None


class FilterBase(BaseModel):
    skip: int
    limit: int


class UserPublic(BaseModel):
    uuid: str
    email: str
    firstname: UpStr
    lastname: UpStr
    middlename: UpStr | None = ""
    phone: str | None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: Any):
        # obfuscate parts of the email with asterisks
        email_parts = value.split("@")
        email_parts[0] = email_parts[0][:5] + "*" * (len(email_parts[0]) - 5)
        email_parts[1] = email_parts[1][:5] + "*" * (len(email_parts[1]) - 5)
        return "@".join(email_parts)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: Any):
        # obfuscate the middle part of the phone with asterisks
        return value[:5] + "*" * (len(value) - 5) + value[-2:]


class UserAccountMin(BaseSchemaMixin):
    user_uuid: str = Field(..., description="unique id of user")
    next_of_kin_uuid: str | None = Field(None, description="unique id of next of kin")
    nin: str | None = Field(None, max_length=16, description="nin of user")
    image: str = Field(..., max_length=255, description="image of user")
    phone: str = Field(..., max_length=20, description="Phone number of the user")
    address: str = Field(..., description="address of user")
    gender: Gender
    birthdate: date

    user: UserMin


class UserAccountPhone(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone: str = Field(..., max_length=20, description="Phone number of the user")


class UserAccountFull(UserAccountMin):
    user: UserMin


class VehicleMin(BaseModel):
    vehicle_id: str
    vehicle_type_id: str
    chassis_number: str | None = None
    engine_number: str | None = None
    license_plate_number: str | None = None


class ConductorMin(BaseModel):
    user_id: str

    user: UserMin


class VehicleConductorMin(BaseModel):
    vehicle_id: str
    conductor_id: str

    vehicle: VehicleMin
    conductor: ConductorMin


class WalletPublic(BaseModelPublic):
    balance: MoneyOut


class PassengerPublic(BaseModelPublic):
    phone_number: str

    user: UserPublic


class CardPublic(BaseModelPublic):
    card_number: str


class PassengerCardPublic(BaseModelPublic):
    passenger: PassengerPublic
    card: CardPublic
