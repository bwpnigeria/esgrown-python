#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2023-06-15 02:31:59
# @Author  : Dahir Muhammad Dahir (dahirmuhammad3@gmail.com)
# @Link    : link
# @Version : 1.0.0


from typing import Any
from fastapi import APIRouter, Depends

from app.dependencies.dependencies import HasPermission
from app.dashboard import schemas, cruds
from app.utils.crud_util import CrudUtil

dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# =================== Super Admin Dashboard ===================


@dashboard_router.get(
    "/super-admin",
    dependencies=[Depends(HasPermission(["superadmin:dashboard"]))],
    response_model=schemas.SuperAdminDashboardOut,
)
async def super_admin_dashboard(
    cu: CrudUtil = Depends(CrudUtil),
    dashboard_in: schemas.SuperAdminDashboardIn = Depends(),
) -> Any:
    return cruds.super_admin_dashboard(cu, dashboard_in)
