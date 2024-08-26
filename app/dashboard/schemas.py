#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2023-06-15 01:22:12
# @Author  : Dahir Muhammad Dahir (dahirmuhammad3@gmail.com)
# @Link    : link
# @Version : 1.0.0


from datetime import date, timedelta
from enum import Enum
from fastapi import HTTPException

from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo

# from app.alumni.schemas import AlumniMin
from app.mixins.schemas import BaseModelIn


class CommonTimeInterval(str, Enum):
    """
    Common time intervals
    """

    yesterday = "yesterday"
    today = "day"
    this_week = "week"
    this_month = "month"
    this_year = "year"
    all_time = "all"
    custom = "custom"


class DashboardIn(BaseModelIn):
    model_config = ConfigDict(str_to_upper=False)
    time_interval: CommonTimeInterval = Field(
        CommonTimeInterval.today,
        description="Time interval to get data for",
        exclude=True,
    )

    from_date: date = Field(
        date.today(),
        description="From date for custom time interval",
        exclude=True,
    )
    to_date: date = Field(
        date.today(),
        description="To date for custom time interval",
        exclude=True,
    )

    @field_validator("from_date")
    @classmethod
    def validate_from_date(cls, v: date | None, info: ValidationInfo) -> date:
        # if time interval is custom, from_date must be provided, else raise error
        if info.data.get("time_interval") == CommonTimeInterval.custom:
            if not v:
                raise HTTPException(
                    status_code=403,
                    detail="from_date is required for custom time interval",
                )
            return v

        # if time interval is any of the other values, then we calculate from_date
        # from the time interval
        time_interval = info.data.get("time_interval")
        if time_interval == CommonTimeInterval.yesterday:
            return date.today() - timedelta(days=1)

        if time_interval == CommonTimeInterval.today:
            return date.today()

        if time_interval == CommonTimeInterval.this_week:
            return date.today() - timedelta(days=date.today().weekday())

        if time_interval == CommonTimeInterval.this_month:
            return date.today().replace(day=1)

        if time_interval == CommonTimeInterval.this_year:
            return date.today().replace(month=1, day=1)

        return date(1970, 1, 1)

    @field_validator("to_date")
    def validate_to_date(cls, v: date | None, info: ValidationInfo) -> date:
        # if time interval is custom, to_date must be provided, else raise error
        if info.data.get("time_interval") == CommonTimeInterval.custom:
            if not v:
                raise HTTPException(
                    status_code=403,
                    detail="to_date is required for custom time interval",
                )
            return v

        # if time interval is any of the other values, then we calculate to_date
        # from the time interval
        time_interval = info.data.get("time_interval")
        if time_interval == CommonTimeInterval.yesterday:
            return date.today() - timedelta(days=1)

        return date.today()


# ==================== Super Admin Dashboard ====================


class SuperAdminDashboardIn(DashboardIn):
    None
    # faculty_id: str | None = Field(None, description="Faculty ID to get data for")
    # department_id: str | None = Field(None, description="Department ID to get data for")


class SuperAdminDashboardOut(BaseModel):
    None
    # alumni_count: int = Field(..., description="Total number of alumni")
    # alumni_profile_claimed: int = Field(
    #     ..., description="Number of alumni with claimed profiles"
    # )
    # alumni_profile_unclaimed: int = Field(
    #     ..., description="Number of alumni with unclaimed profiles"
    # )

    # recent_alumni: list[AlumniMin] | None = Field(
    #     None, description="A list of recent alumni that claimed their profiles"
    # )
