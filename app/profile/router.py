#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2024-08-26 15:30
# @Author  : Nasir Lawal (nasirlawal001@gmail.com)
# @Link    : link
# @Version : 1.0.0


from typing import Any
from fastapi import APIRouter, Body, Depends, File, UploadFile
from app.user.schemas import UserSchema

from app.profile import schemas, cruds
from app.utils.crud_util import CrudUtil
from app.dependencies.dependencies import (
    HasPermission,
    get_current_user,
    get_super_user,
)
from app.utils.custom_validators import UpStr

individual_router = APIRouter(
    prefix="/individual",
    tags=["Individual Routes"],
)


# ======================[ Individual ]=======================

@individual_router.post(
    "",
)
async def create_profile(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    individual: schemas.IndividualIn,
) -> schemas.IndividualOut:
    return cruds.create_profile(cu, individual)


@individual_router.get(
    "",
    dependencies=[Depends(HasPermission(["individual:list"]))],
    response_model=schemas.IndividualList,
)
async def list_individuals(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    filter: schemas.IndividualFilter = Depends(),
) -> Any:
    return cruds.get_all_profile(cu, filter)


@individual_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["individual:read"]))],
)
async def get_profile(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> schemas.IndividualOut:
    return cruds.get_profile(cu, uuid)


@individual_router.get(
    "/own/profile",
    dependencies=[Depends(HasPermission(["individual:read_own_profile"]))],
)
async def get_own_profile(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    user: UserSchema = Depends(get_current_user),
) -> schemas.IndividualOut:
    return cruds.get_own_profile(cu, user)


@individual_router.put(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["individual:update"]))],
)
async def update_profile(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    individual: schemas.IndividualUpdate,
) -> schemas.IndividualOut:
    return cruds.update_profile(cu, uuid, individual)


@individual_router.put(
    "/own/profile",
    dependencies=[Depends(HasPermission(["individual:update_own_profile"]))],
)
async def update_own_profile(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    user: UserSchema = Depends(get_current_user),
    individual: schemas.IndividualUpdate,
) -> schemas.IndividualOut:
    return cruds.update_own_profile(cu, individual, user)


@individual_router.get(
    "/search/all/profile",
    dependencies=[Depends(HasPermission(["individual:search"]))],
    response_model=schemas.IndividualList,
)
async def search_profile(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    search: schemas.IndividualSearch = Depends(),
) -> Any:
    return cruds.search_profile(cu, search)



@individual_router.delete(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["individual:delete"]))],
)
async def delete_profile(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> dict[str, Any]:
    return cruds.delete_profile(cu, uuid)