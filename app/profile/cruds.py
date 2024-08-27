#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2024-08-26 15:30
# @Author  : Nasir Lawal (nasirlawal001@gmail.com)
# @Link    : link
# @Version : 1.0.0

from typing import Any
from fastapi import HTTPException, UploadFile
from sqlalchemy import and_, or_
from app.access_control.cruds import get_group_by_name
from app.mixins.commons import Gender
from app.mixins.schemas import OrderType
from app.user.cruds import create_user, delete_user, update_user
from app.user.models import User
from app.utils.crud_util import CrudUtil
from app.profile import models, schemas
from app.user.schemas import UserIn, UserSchema
from app.utils.custom_validators import UpStr, make_capitalize
from app.utils.user import get_password_hash
from app.utils.image_qr import (
    upload_image_file_to_cloud,
)

def create_profile(
    cu: CrudUtil,
    individual: schemas.IndividualIn,
) -> schemas.IndividualOut | models.Individual:
    # Ensure profile is unique
    cu.ensure_unique_model(
        models.Individual,
        {"email": individual.email, "phone": individual.phone},
    )

    # Hash the password
    hashed_password = get_password_hash(password=individual.password)

    # Create the individual model
    individual_request: models.Individual = cu.create_model(
        models.Individual,
        schemas.IndividualCreate(
            **individual.model_dump(),
            password_hash=hashed_password,
        ),
    )

    return individual_request


def upload_own_photo(
    cu: CrudUtil,
    photo: UploadFile,
    user: UserSchema,
) -> schemas.IndividualOut | models.Individual:
    db_individual: models.Individual = get_own_profile(cu, user)

    photo_url: str = upload_image_file_to_cloud(
        photo,
        subfolder="esgrown-db-images/",
        resize=False,
    )

    db_individual.photo = photo_url

    cu.db.commit()
    cu.db.refresh(db_individual)

    return db_individual

def get_profile(
    cu: CrudUtil,
    uuid: str,
) -> schemas.IndividualOut | models.Individual:
    # get the individual
    db_individual: models.Individual = cu.get_model_or_404(
        models.Individual,
        {"uuid": uuid},
    )

    return db_individual

def get_own_profile(
    cu: CrudUtil,
    user: UserSchema,
) -> schemas.IndividualOut | models.Individual:
    # get the individual
    db_individual: models.Individual = cu.get_model_or_404(
        models.Individual,
        {"user_id": user.uuid},
    )

    return db_individual

def get_individual_by_user_id(
    cu: CrudUtil,
    user_id: str,
) -> schemas.IndividualOut | models.Individual:
    db_individual: models.Individual = cu.get_model_or_404(
        models.Individual,
        {"user_id": user_id},
    )
    return db_individual

def get_all_profile(
    cu: CrudUtil,
    filter: schemas.IndividualFilter
) -> Any:
    return cu.list_model(
        models.Individual,
        filter.model_dump(exclude_unset=True),
    )


def update_profile(
    cu: CrudUtil,
    uuid: str,
    individual: schemas.IndividualUpdate,
) -> schemas.IndividualOut | models.Individual:
    db_individual: models.Individual = cu.get_model_or_404(
        models.Individual,
        {"uuid": uuid},
    )

    db_individual: models.Individual = cu.update_model(
        models.Individual,
        individual,
        {"uuid": uuid},
    )

    return db_individual


def update_own_profile(
    cu: CrudUtil,
    profile: schemas.IndividualUpdate,
    user: UserSchema,
) -> schemas.IndividualOut | models.Individual:
    db_profile: models.Individual = cu.get_model_or_404(
        models.Individual,
        {"user_id": user.uuid},
    )


    if profile.user:
        update_user(
            cu,
            str(db_profile.user.uuid),
            profile.user,
            autocommit=False,
        )
    db_profile.address = profile.address or db_profile.address  # type: ignore
    db_profile.date_of_birth = profile.date_of_birth or db_profile.date_of_birth  # type: ignore
    db_profile.gender = profile.gender or db_profile.gender  # type: ignore

    cu.db.commit()
    cu.db.refresh(db_profile)

    return db_profile


def search_profile(
    cu: CrudUtil,
    search: schemas.IndividualSearch
) -> Any:
    return cu.search_model(
        models.Individual,
        search.search,
        search.search_fields,
        join_search=search.join_search,
        skip=search.skip,
        limit=search.limit,
        order=search.order,
    )

# def list_profile(
#     cu: CrudUtil,
#     filter: schemas.IndividualFilter,
# ) -> Any:
#     return cu.list_model(
#         models.Individual,
#         filter.model_dump(exclude_unset=True),
#     )

# def search_profile(
#     cu: CrudUtil,
#     search: schemas.IndividualSearch,
# ) -> Any:
#     return cu.search_model(
#         models.Individual,
#         search.search,
#         search.search_fields,
#         join_search=search.join_search,
#         skip=search.skip,
#         limit=search.limit,
#         order=search.order,
#     )

# def delete_profile(
#     cu: CrudUtil,
#     uuid: str,
# ) -> dict[str, Any]:
#     db_profile: models.Individual = cu.get_model_or_404(
#         models.Individual,
#         {"uuid": uuid},
#     )

#     # we remove the user group
#     try:
#         db_profile.user.groups.remove(get_group_by_name(cu, "normal_user_group"))
#     except ValueError:
#         pass

#     # now delete the profile
#     cu.delete_model(
#         models.Individual,
#         {"uuid": uuid},
#         autocommit=False,
#     )

#     return delete_user(
#         cu,
#         str(db_profile.user_id),
#         autocommit=True,
#     )