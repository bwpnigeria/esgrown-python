#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2023-10-25 02:22:34
# @Author  : Dahir Muhammad Dahir (dahirmuhammad3@gmail.com)
# @Link    : link
# @Version : 1.0.0


from typing import Any
from fastapi import APIRouter, Depends
from app.user.schemas import UserSchema

from app.lga import schemas, cruds
from app.utils.crud_util import CrudUtil
from app.dependencies.dependencies import HasPermission, get_current_user


country_router = APIRouter(
    prefix="/country",
    tags=["Country Routes"],
)

state_router = APIRouter(
    prefix="/state",
    tags=["State Routes"],
)

lga_router = APIRouter(
    prefix="/lga",
    tags=["Local Government Routes"],
)

# ======================[ Country ]=======================


@country_router.post(
    "",
    dependencies=[Depends(HasPermission(["country:create"]))],
)
async def create_country(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    country: schemas.CountryIn,
    user: UserSchema = Depends(get_current_user),
) -> schemas.CountryOut:
    return cruds.create_country(cu, country, user)


@country_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["country:read"]))],
)
async def get_country(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> schemas.CountryOut:
    return cruds.get_country(cu, uuid)


@country_router.get(
    "/name/{name}",
    dependencies=[Depends(HasPermission(["country:read"]))],
)
async def get_country_by_name(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    name: str,
) -> schemas.CountryOut:
    return cruds.get_country_by_name(cu, name)


@country_router.put(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["country:update"]))],
)
async def update_country(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    country: schemas.CountryUpdate,
) -> schemas.CountryOut:
    return cruds.update_country(cu, uuid, country)


@country_router.get(
    "",
    # dependencies=[Depends(HasPermission(["state:list"]))],
    response_model=schemas.CountryList,
)
async def list_countries(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    filter: schemas.CountryFilter = Depends(),
) -> Any:
    return cruds.list_countries(cu, filter)


@country_router.delete(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["country:delete"]))],
)
async def delete_country(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> dict[str, Any]:
    return cruds.delete_country(cu, uuid)



# ======================[ State ]=======================


@state_router.post(
    "",
    dependencies=[Depends(HasPermission(["state:create"]))],
)
async def create_state(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    state: schemas.StateIn,
    user: UserSchema = Depends(get_current_user),
) -> schemas.StateOut:
    return cruds.create_state(cu, state, user)


@state_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["state:read"]))],
)
async def get_state(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> schemas.StateOut:
    return cruds.get_state(cu, uuid)


@state_router.get(
    "/name/{name}",
    dependencies=[Depends(HasPermission(["state:read"]))],
)
async def get_state_by_name(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    name: str,
) -> schemas.StateOut:
    return cruds.get_state_by_name(cu, name)


@state_router.put(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["state:update"]))],
)
async def update_state(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    state: schemas.StateUpdate,
) -> schemas.StateOut:
    return cruds.update_state(cu, uuid, state)


@state_router.get(
    "",
    # dependencies=[Depends(HasPermission(["state:list"]))],
    response_model=schemas.StateList,
)
async def list_states(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    filter: schemas.StateFilter = Depends(),
) -> Any:
    return cruds.list_states(cu, filter)


@state_router.delete(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["lga:delete"]))],
)
async def delete_state(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> dict[str, Any]:
    return cruds.delete_state(cu, uuid)


# ======================[ Local Government ]=======================


@lga_router.post(
    "",
    dependencies=[Depends(HasPermission(["lga:create"]))],
)
async def create_local_government(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    local_government: schemas.LocalGovernmentIn,
    user: UserSchema = Depends(get_current_user),
) -> schemas.LocalGovernmentOut:
    return cruds.create_local_government(cu, local_government, user)


@lga_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["lga:read"]))],
)
async def get_local_government(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> schemas.LocalGovernmentOut:
    return cruds.get_local_government(cu, uuid)


@lga_router.get(
    "/name/{name}",
    dependencies=[Depends(HasPermission(["lga:read"]))],
)
async def get_local_government_by_name(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    name: str,
) -> schemas.LocalGovernmentOut:
    return cruds.get_local_government_by_name(cu, name)


@lga_router.put(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["lga:update"]))],
)
async def update_local_government(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    local_government: schemas.LocalGovernmentUpdate,
) -> schemas.LocalGovernmentOut:
    return cruds.update_local_government(cu, uuid, local_government)


@lga_router.get(
    "",
    # dependencies=[Depends(HasPermission(["lga:list"]))],
    response_model=schemas.LocalGovernmentList,
)
async def list_local_governments(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    filter: schemas.LocalGovernmentFilter = Depends(),
) -> Any:
    return cruds.list_local_governments(cu, filter)


@lga_router.delete(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["lga:delete"]))],
)
async def delete_local_government(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> Any:
    return cruds.delete_local_government(cu, uuid)
