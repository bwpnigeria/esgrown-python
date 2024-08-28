#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-09-19 22:37:46
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from typing import Any
from fastapi.param_functions import Path
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends

from app.access_control.cruds import get_group_by_name
from app.dependencies import dependencies as deps
from app.user import cruds, schemas
from app.utils.crud_util import CrudUtil
from app.utils.user import create_access_token, create_mobile_access_token


users_router = APIRouter(
    prefix="/users", tags=["User"], dependencies=[Depends(deps.get_current_user)]
)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post(
    "/docs-token",
    include_in_schema=False,
)
def docs_authentication(
    cu: CrudUtil = Depends(CrudUtil),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.Token:
    user = cruds.authenticate_user(
        cu=cu, email_or_phone=str(form_data.username), password=form_data.password
    )

    token_data_to_encode = {
        "data": {
            "uuid": user.uuid,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "permissions": user.permissions,
        }
    }
    access_token = create_access_token(token_data_to_encode)
    return schemas.Token(access_token=access_token, token_type="bearer")


@auth_router.post(
    "/token",
    response_model=schemas.Token,
)
def login(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    user_data: schemas.Login,
) -> schemas.Token:
    user: schemas.UserSchema = cruds.authenticate_user(
        cu,
        str(user_data.email_or_phone),
        user_data.password,
    )

    token_data_to_encode = {
        "data": {
            "uuid": user.uuid,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "user_group": user.groups[0].name if user.groups else None,
        }
    }

    access_token = create_access_token(token_data_to_encode)
    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
        permissions=user.permissions,
    )


@auth_router.post(
    "/mobile/token",
    response_model=schemas.Token,
)
def mobile_login(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    user_data: schemas.Login,
) -> schemas.Token:
    user: schemas.UserSchema = cruds.authenticate_user(
        cu,
        str(user_data.email_or_phone),
        user_data.password,
    )

    token_data_to_encode = {
        "data": {
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "user_group": user.groups[0].name if user.groups else None,
        }
    }

    access_token = create_mobile_access_token(token_data_to_encode)
    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
        permissions=user.permissions,
    )


@auth_router.post("/reset-password/{email_or_phone}")
def reset_password(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    email_or_phone: str,
) -> dict[str, Any]:
    return cruds.reset_password(cu, email_or_phone)


@users_router.post(
    "", status_code=201, dependencies=[Depends(deps.HasPermission(["admin:create"]))]
)
def create_admin_user(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    user_data: schemas.UserIn,
) -> schemas.UserSchema:
    return cruds.create_user(cu, user_data, is_admin=True)


@users_router.post(
    "/user-account", 
    status_code=201, dependencies=[Depends(deps.HasPermission(["account:create"]))]
)
def create_user_account(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    user_data: schemas.UserAccountIn,
) -> schemas.UserSchema:
    return cruds.create_user_account(cu, user_data, is_admin=False, can_login=True)


@users_router.get(
    "",
    response_model=schemas.UserList,
    dependencies=[Depends(deps.HasPermission(["admin:list"]))],
)
def list_admin_users(
    cu: CrudUtil = Depends(CrudUtil),
    filter: schemas.AdminUserFilter = Depends(),
    skip: int = 0,
    limit: int = 100,
) -> schemas.UserList:
    return cruds.list_admin_users(cu, filter, skip=skip, limit=limit)


@users_router.get("/{uuid}", dependencies=[Depends(deps.HasPermission(["admin:read"]))])
def get_admin_detail(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> schemas.UserSchema:
    return cruds.get_user_by_uuid(cu, uuid)


@users_router.put(
    "/{uuid}", dependencies=[Depends(deps.HasPermission(["admin:update"]))]
)
def update_admin(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    user_data: schemas.UserUpdate,
) -> schemas.UserSchema:
    return cruds.update_user(cu, uuid, user_data)


@users_router.put(
    "/change_password/{user_uuid}",
    dependencies=[Depends(deps.HasPermission(["admin:update"]))],
)
def change_admin_password(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    user_uuid: str = Path(...),
) -> schemas.PasswordChangeOut:
    return cruds.change_admin_password(cu, user_uuid)


@users_router.put(
    "/own/change_password",
    dependencies=[Depends(deps.HasPermission(["user:change_own_password"]))],
)
def change_own_password(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    user: schemas.UserSchema = Depends(deps.get_current_user),
) -> schemas.PasswordChangeOut:
    return cruds.change_own_password(cu, user)


@users_router.delete(
    "/{uuid}", dependencies=[Depends(deps.HasPermission(["admin:delete"]))]
)
def delete_admin(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> dict[str, Any]:
    return cruds.delete_user(cu, uuid)


@users_router.post(
    "/{uuid}/groups", dependencies=[Depends(deps.HasPermission(["admin:update"]))]
)
def add_group_to_user(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    groups: schemas.UserGroup,
) -> schemas.UserSchema:
    user = cruds.get_user_by_uuid(cu, uuid)
    group_list = groups.model_dump().pop("groups")

    for group_name in group_list:
        group = get_group_by_name(cu, name=group_name)
        user.groups.append(group)

    cu.db.commit()
    cu.db.refresh(user)
    return user


@users_router.delete(
    "/{uuid}/groups/{group_name}",
    dependencies=[Depends(deps.HasPermission(["admin:update"]))],
)
def remove_group_from_user(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    group_name: str,
) -> schemas.UserSchema:
    user = cruds.get_user_by_uuid(cu, uuid=uuid)

    group = get_group_by_name(cu, group_name)
    user.groups.remove(group)

    cu.db.commit()
    cu.db.refresh(user)
    return user
