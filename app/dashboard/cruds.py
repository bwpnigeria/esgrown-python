#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2023-06-15 04:22:01
# @Author  : Dahir Muhammad Dahir (dahirmuhammad3@gmail.com)
# @Link    : link
# @Version : 1.0.0


from typing import Any
# from app.alumni.models import Alumni
# from app.alumni.schemas import AlumniFilter
from app.dashboard import schemas

# from app.mixins.commons import DateRange
from app.utils.crud_util import CrudUtil
# from app.utils.enums import AlumniProfileStatus


# ==================== Super Admin Dashboard ====================


def super_admin_dashboard(
    cu: CrudUtil,
    dashboard_in: schemas.SuperAdminDashboardIn,
) -> dict[str, Any]:
    # conditions: dict[str, Any] = {
    #     **dashboard_in.model_dump(exclude_unset=True),
    # }

    # alumni_count: int = cu.list_model(
    #     Alumni,
    #     conditions,
    #     limit=1,
    # )["count"]

    # claimed_filter = AlumniFilter(
    #     **conditions,
    #     profile_status=AlumniProfileStatus.claimed,
    # )

    # alumni_profile_claimed: int = cu.get_model_count(
    #     Alumni,
    #     column_to_count_by="id",
    #     model_conditions=claimed_filter.model_dump(exclude_unset=True),
    # )

    # alumni_profile_unclaimed: int = alumni_count - alumni_profile_claimed

    # recent_alumni = cu.list_model(
    #     Alumni,
    #     {},
    #     limit=5,
    #     order="desc",
    # )["items"]

    # return {
    #     "alumni_count": alumni_count,
    #     "alumni_profile_claimed": alumni_profile_claimed,
    #     "alumni_profile_unclaimed": alumni_profile_unclaimed,
    #     "recent_alumni": recent_alumni,
    # }
    return None
