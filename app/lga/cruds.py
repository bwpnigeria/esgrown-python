#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2023-10-25 01:01:42
# @Author  : Dahir Muhammad Dahir (dahirmuhammad3@gmail.com)
# @Link    : link
# @Version : 1.0.0


from typing import Any

from app.utils.crud_util import CrudUtil

from app.lga import models, schemas
from app.user.schemas import UserSchema


# ======================[ State ]=======================


def create_state(
    cu: CrudUtil,
    state: schemas.StateIn,
    user: UserSchema,
) -> schemas.StateOut | models.State:
    # ensure unique state name
    cu.ensure_unique_model(
        models.State,
        {"name": state.name},
    )

    # now create the state
    db_state: models.State = cu.create_model(
        models.State,
        schemas.StateCreate(
            **state.model_dump(),
            created_by=user.uuid,
        ),
    )

    return db_state


def get_state(
    cu: CrudUtil,
    uuid: str,
) -> schemas.StateOut | models.State:
    # get the state
    db_state: models.State = cu.get_model_or_404(
        models.State,
        {"uuid": uuid},
    )

    return db_state


def get_state_by_name(
    cu: CrudUtil,
    name: str,
) -> schemas.StateOut | models.State:
    # get the state
    db_state: models.State = cu.get_model_or_404(
        models.State,
        {"name": name},
    )

    return db_state


def get_all_states(
    cu: CrudUtil,
) -> list[schemas.StateOut] | list[models.State]:
    states: list[models.State] = cu.list_model(
        models.State,
        {},
    )["items"]

    return states


def update_state(
    cu: CrudUtil,
    uuid: str,
    state: schemas.StateUpdate,
) -> schemas.StateOut | models.State:
    db_state: models.State = cu.update_model(
        models.State,
        state,
        {"uuid": uuid},
    )

    return db_state


def list_states(
    cu: CrudUtil,
    filter: schemas.StateFilter,
) -> Any:
    return cu.list_model(
        models.State,
        filter.model_dump(exclude_unset=True),
    )


def delete_state(
    cu: CrudUtil,
    uuid: str,
) -> dict[str, Any]:
    return cu.delete_model(
        models.State,
        {"uuid": uuid},
    )


# ======================[ Local Government ]=======================


def create_local_government(
    cu: CrudUtil,
    local_government: schemas.LocalGovernmentIn,
    user: UserSchema,
) -> schemas.LocalGovernmentOut | models.LocalGovernment:
    # ensure unique local government name
    cu.ensure_unique_model(
        models.LocalGovernment,
        {"name": local_government.name},
    )

    # now create the local government
    db_local_government: models.LocalGovernment = cu.create_model(
        models.LocalGovernment,
        schemas.LocalGovernmentCreate(
            **local_government.model_dump(),
            created_by=user.uuid,
        ),
    )

    return db_local_government


def get_local_government(
    cu: CrudUtil,
    uuid: str,
) -> schemas.LocalGovernmentOut | models.LocalGovernment:
    # get the local government
    db_local_government: models.LocalGovernment = cu.get_model_or_404(
        models.LocalGovernment,
        {"uuid": uuid},
    )

    return db_local_government


def get_local_government_by_name(
    cu: CrudUtil,
    name: str,
) -> schemas.LocalGovernmentOut | models.LocalGovernment:
    # get the local government
    db_local_government: models.LocalGovernment = cu.get_model_or_404(
        models.LocalGovernment,
        {"name": name},
    )

    return db_local_government


def update_local_government(
    cu: CrudUtil,
    uuid: str,
    local_government: schemas.LocalGovernmentUpdate,
) -> schemas.LocalGovernmentOut | models.LocalGovernment:
    db_local_government: models.LocalGovernment = cu.update_model(
        models.LocalGovernment,
        local_government,
        {"uuid": uuid},
    )

    return db_local_government


def list_local_governments(
    cu: CrudUtil,
    filter: schemas.LocalGovernmentFilter,
) -> Any:
    return cu.list_model(
        models.LocalGovernment,
        filter.model_dump(exclude_unset=True),
    )


def delete_local_government(
    cu: CrudUtil,
    uuid: str,
) -> dict[str, Any]:
    return cu.delete_model(
        models.LocalGovernment,
        {"uuid": uuid},
    )
