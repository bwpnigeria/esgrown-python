#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-06-22 06:52:50
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from datetime import date
from decimal import Decimal
from typing import Annotated, Any, Optional
from fastapi.exceptions import HTTPException
from pydantic import AfterValidator, condecimal
from textblob import TextBlob


# convert from naira to kobo, as all
# values in database should be in kobo
def currency_in(amount: Decimal) -> Optional[Decimal]:
    if amount is not None:
        return amount * 100

    return None


# convert from kobo back to naira
def currency_out(amount: Decimal) -> Optional[Decimal]:
    if amount is not None:
        return amount / 100
    return None


PositiveDecimal = condecimal(ge=0)

MoneyIn = Annotated[Decimal, AfterValidator(currency_in)]
MoneyOut = Annotated[Decimal | Any, AfterValidator(currency_out)]
Money = Annotated[Decimal | Any, "Money"]


def make_uppercase(value: str) -> Optional[str]:
    if value is not None:
        return value.upper()
    return None


def make_lowercase(value: str) -> Optional[str]:
    if value is not None:
        return value.lower()
    return None


def make_capitalize(value: str) -> Optional[str]:
    if value is not None:
        if value.isupper() or value.islower():
            blob = TextBlob(value)
            return str(blob.title())

        return value


def reg_number_out(value: str) -> str:
    if "UNAVAILABLE" in value:
        return "UNAVAILABLE"

    return value


UpStr = Annotated[str, AfterValidator(make_uppercase)]
LowStr = Annotated[str, AfterValidator(make_lowercase)]
CapStr = Annotated[str, AfterValidator(make_capitalize)]
RegOut = Annotated[str, AfterValidator(reg_number_out)]


def check_is_18_above(value: date) -> date | None:
    if not value:
        return None

    if date.today().year - value.year < 18:
        raise HTTPException(403, detail="Age must 18 years or above to register")

    return value


LegalBirthdate = Annotated[date | None, AfterValidator(check_is_18_above)]


def clean_string(value: str) -> Optional[str]:
    if value is not None:
        return (
            value.replace(" ", "")
            .replace("-", "")
            .replace("_", "")
            .replace("/", "")
            .replace("\\", "")
            .upper()
        )

    return None


CleanStr = Annotated[str | None, AfterValidator(clean_string)]
