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

from app.profile import schemas, cruds, models
from app.utils.crud_util import CrudUtil
from app.dependencies.dependencies import (
    HasPermission,
    get_current_user,
)

individual_router = APIRouter(
    prefix="/individual",
    tags=["Individual Routes"],
)

corporate_router = APIRouter(
    prefix="/corporate",
    tags=["Corporate Routes"],
)

subject_router = APIRouter(
    prefix="/subject",
    tags=["Subject Routes"],
)

class_router = APIRouter(
    prefix="/class",
    tags=["Class Routes"],
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
    dependencies=[Depends(HasPermission(["admin:list_individual"]))],
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
    dependencies=[Depends(HasPermission(["admin:read_individual"]))],
)
async def get_profile(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> schemas.IndividualOut:
    return cruds.get_profile(cu, uuid)


@individual_router.get(
    "/own/profile",
    dependencies=[Depends(HasPermission(["individual:read_individual_own_profile"]))],
)
async def get_own_profile(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    user: UserSchema = Depends(get_current_user),
) -> schemas.IndividualOut:
    return cruds.get_own_profile(cu, user)


@individual_router.put(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["admin:update_individual"]))],
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
    individual: schemas.IndividualUpdateSelf,
) -> schemas.IndividualOut:
    return cruds.update_own_profile(cu, individual, user)


@individual_router.get(
    "/search/all/profile",
    dependencies=[Depends(HasPermission(["admin:search_individual"]))],
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
    dependencies=[Depends(HasPermission(["admin:delete_individual"]))],
)
async def delete_profile(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> dict[str, Any]:
    return cruds.delete_profile(cu, uuid)


# ================ Corporate ================
@corporate_router.post(
    "",
)
async def create_corporate(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    corporate: schemas.CorporateIn,
) -> schemas.CorporateOut:
    return cruds.create_corporate(cu, corporate)


@corporate_router.get(
    "",
    dependencies=[Depends(HasPermission(["admin:list_corporate"]))],
    response_model=schemas.CorporateList,
)
async def list_corporates(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    filter: schemas.CorporateFilter = Depends(),
) -> Any:
    return cruds.get_all_corporate(cu, filter)


@corporate_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["admin:read_corporate"]))],
)
async def get_corporate(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> schemas.CorporateOut:
    return cruds.get_corporate(cu, uuid)


@corporate_router.get(
    "/own/corporate",
    dependencies=[Depends(HasPermission(["corporate:read_corporate_own_profile"]))],
)
async def get_own_corporate(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    user: UserSchema = Depends(get_current_user),
) -> schemas.CorporateOut:
    return cruds.get_own_corporate(cu, user)


@corporate_router.put(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["admin:update_corporate"]))],
)
async def update_corporate(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    corporate: schemas.CorporateUpdate,
) -> schemas.CorporateOut:
    return cruds.update_corporate(cu, uuid, corporate)


@corporate_router.put(
    "/own/corporate",
    dependencies=[Depends(HasPermission(["corporate:update_own_corporate"]))],
)
async def update_own_corporate(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    user: UserSchema = Depends(get_current_user),
    corporate: schemas.CorporateUpdateSelf,
) -> schemas.CorporateOut:
    return cruds.update_own_corporate(cu, corporate, user)


@corporate_router.delete(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["admin:delete_corporate"]))],
)
async def delete_corporate(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> dict[str, Any]:
    return cruds.delete_corporate(cu, uuid)


@corporate_router.get(
    "/search/all/corporate",
    dependencies=[Depends(HasPermission(["admin:search_corporate"]))],
    response_model=schemas.CorporateList,
)
async def search_corporate(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    search: schemas.CorporateSearch = Depends(),
) -> Any:
    return cruds.search_corporate(cu, search)


# ================ Subject ================

@subject_router.post(
    "",
    dependencies=[Depends(HasPermission(["subject:create"]))],
)
async def create_subject(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    subject_data: schemas.SubjectCreate
) -> schemas.SubjectSchema:
    return cruds.create_subject(cu, subject_data)


@subject_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["subject:read"]))],
)
def subject_detail(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> schemas.SubjectSchema:
    return cruds.get_subject_by_uuid(cu, uuid)


@subject_router.put(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["subject:update"]))],
)
def update_subject(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    subject_data: schemas.SubjectUpdate,
) -> schemas.SubjectSchema:
    return cruds.update_subject(cu, uuid, subject_data)


@subject_router.get(
    "",
    dependencies=[Depends(HasPermission(["subject:list"]))],
)
def subject_list(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    skip: int = 0,
    limit: int = 100,
) -> schemas.SubjectList:
    return cruds.list_subject(cu, skip, limit)


@subject_router.delete(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["subject:delete"]))],
)
def delete_subject(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> dict[str, Any]:
    return cruds.delete_subject(cu, uuid)


# ================ Classes ================

@class_router.post(
    "",
    dependencies=[Depends(HasPermission(["class:create"]))],
)
def create_class(
    class_data: schemas.ClassCreate,
    cu: CrudUtil = Depends(CrudUtil),
) -> schemas.ClassSchema:
    return cruds.create_class(cu, class_data)


@class_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["class:read"]))],
)
def class_detail(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> schemas.ClassSchema:
    return cruds.get_class_by_uuid(cu, uuid)

@class_router.get(
    "",
    dependencies=[Depends(HasPermission(["class:list"]))],
)
def class_list(
    cu: CrudUtil = Depends(CrudUtil),
    skip: int = 0,
    limit: int = 100,
) -> schemas.ClassList:
    return cruds.list_class(cu, skip, limit)


@class_router.put(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["class:update"]))],
)
def update_class(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    update_data: schemas.ClassUpdate,
) -> schemas.ClassSchema:
    return cruds.update_class(cu, uuid, update_data)


@class_router.delete(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["class:delete"]))],
)
def delete_class(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str
) -> dict[str, Any]:
    return cruds.delete_class(cu, uuid)


@class_router.delete(
    "/{uuid}/subjects",
    dependencies=[Depends(HasPermission(["class:update"]))],
)
def remove_subject_from_class(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    subj_to_delete: schemas.RemoveClassSubject,
) -> schemas.ClassSchema:
    db_class = cruds.get_class_by_uuid(cu, uuid)
    subjects = subj_to_delete.model_dump()["subjects"]
    for subj_uuid in subjects:
        subj = cruds.get_subject_by_uuid(cu, uuid=subj_uuid)
        if subj:
            try:
                db_class.subjects.remove(subj)
            except ValueError:
                pass

    cu.db.commit()
    cu.db.refresh(db_class)
    return db_class