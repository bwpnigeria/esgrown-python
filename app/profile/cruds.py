#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2024-08-26 15:30
# @Author  : Nasir Lawal (nasirlawal001@gmail.com)
# @Link    : link
# @Version : 1.0.0

from typing import Any
from fastapi import HTTPException, UploadFile
from app.access_control.cruds import get_group_by_name
from app.user.cruds import update_user, create_user_account, delete_user
from app.utils.crud_util import CrudUtil
from app.profile import models, schemas
from app.user.schemas import  UserSchema
from app.utils.image_qr import (
    upload_image_file_to_cloud,
)
from datetime import datetime, date, timedelta
from app.mixins.commons import DateRange

# ====================[ Private ]====================

def create_profile(
    cu: CrudUtil,
    individual: schemas.IndividualIn,
) -> schemas.IndividualOut | models.Individual:
    
    user = create_user_account(
        cu,
        user_data= individual.user,
        autocommit=False,
        can_login=True,
    )

    try:
        user.groups.append(get_group_by_name(cu, "private_user_group"))
    except Exception:
        cu.db.rollback()
        raise HTTPException(
            status_code=403,
            detail="User group not found, it should be created",
        )
    
    # Create the individual model
    db_profile: models.Individual = cu.create_model(
        models.Individual,
        schemas.IndividualCreate(
            user_id=str(user.uuid),
            user=user,
            **individual.model_dump(exclude={"user"}),
        ),
    )

    return db_profile


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
    # get the individual from database
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

    if individual.user:
        update_user(
            cu,
            str(db_individual.user.uuid),
            individual.user,
            autocommit=False,
        )

    db_individual: models.Individual = cu.update_model(
        models.Individual,
        individual,
        {"uuid": uuid},
    )

    if individual.employers:
        for employer in individual.employers:
            db_individual.employers.append(
                get_corporate(cu, uuid=employer)
            )

    cu.db.commit()
    cu.db.refresh(db_individual)

    return db_individual


def update_own_profile(
    cu: CrudUtil,
    profile: schemas.IndividualUpdateSelf,
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

    db_profile: models.Individual = cu.update_model(
        models.Individual,
        profile,
        {"uuid": db_profile.uuid},
    )

    if profile.employers:
        for employer in profile.employers:
            db_profile.employers.append(
                get_corporate(cu, uuid=employer)
            )

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


def delete_profile(
    cu: CrudUtil,
    uuid: str,
) -> dict[str, Any]:

    db_individual: models.Individual = cu.get_model_or_404(
        models.Individual,
        {"uuid": uuid},
    )

    try:
        db_individual.user.groups.remove(get_group_by_name(cu, "private_user_group"))
    except ValueError:
        pass

    # now delete the profile
    cu.delete_model(
        models.Individual,
        {"uuid": uuid},
    )

    return delete_user(
        cu,
        str(db_individual.user.uuid),
        autocommit=True
    )


# ====================[ Corporate ]====================

def create_corporate(
    cu: CrudUtil,
    corporate: schemas.CorporateIn,
) -> schemas.CorporateOut | models.Corporate:
    user = create_user_account(
        cu,
        user_data=corporate.user,
        autocommit=False,
        can_login=True,
    )

    try:
        user.groups.append(get_group_by_name(cu, "corporate_user_group"))
    except Exception:
        cu.db.rollback()
        raise HTTPException(
            status_code=403,
            detail="User group not found, it should be created",
        )

    # Create the individual model
    db_corporate: models.Corporate = cu.create_model(
        models.Corporate,
        schemas.CorporateCreate(
            user_id=str(user.uuid),
            user=user,
            **corporate.model_dump(exclude={"user"}),
        ),
    )

    return db_corporate


def get_corporate(
    cu: CrudUtil,
    uuid: str,
) -> schemas.CorporateOut | models.Corporate:
    # get the individual from database
    db_corporate: models.Corporate = cu.get_model_or_404(
        models.Corporate,
        {"uuid": uuid},
    )

    return db_corporate


def get_all_corporate(
    cu: CrudUtil,
    filter: schemas.CorporateFilter,
) -> Any:
    return cu.list_model(
        models.Corporate,
        filter.model_dump(exclude_unset=True),
    )


def get_own_corporate(
    cu: CrudUtil,
    user: UserSchema,
) -> schemas.CorporateOut | models.Corporate:
    # get the corporate from database
    db_corporate: models.Corporate = cu.get_model_or_404(
        models.Corporate,
        {"user_id": user.uuid},
    )

    return db_corporate


def update_corporate(
    cu: CrudUtil,
    uuid: str,
    corporate: schemas.CorporateUpdate,
) -> schemas.CorporateOut | models.Corporate:
    db_corporate: models.Corporate = cu.get_model_or_404(
        models.Corporate,
        {"uuid": uuid},
    )

    if corporate.user:
        update_user(
            cu,
            str(db_corporate.user.uuid),
            corporate.user,
            autocommit=False,
        )

    if corporate.classes:
        for classroom in corporate.classes:
            db_corporate.classes.append(
                get_class_by_uuid(cu, uuid=classroom)
            )

    if corporate.employees:
        for employee in corporate.employees:
            db_corporate.employees.append(
                get_corporate(cu, uuid=employee)
            )

    db_corporate: models.Corporate = cu.update_model(
        models.Corporate,
        corporate,
        {"uuid": uuid},
    )

    return db_corporate


def update_own_corporate(
    cu: CrudUtil,
    corporate: schemas.CorporateUpdateSelf,
    user: UserSchema,
) -> schemas.CorporateOut | models.Corporate:
    db_corporate: models.Corporate = cu.get_model_or_404(
        models.Corporate,
        {"user_id": user.uuid},
    )

    if corporate.user:
        update_user(
            cu,
            str(db_corporate.user.uuid),
            corporate.user,
            autocommit=False,
        )

    if corporate.classes:
        for classroom in corporate.classes:
            db_corporate.classes.append(
                get_class_by_uuid(cu, uuid=classroom)
            )

    if corporate.employees:
        for employee in corporate.employees:
            db_corporate.employees.append(
                get_profile(cu, uuid=employee)
            )

    db_corporate: models.Corporate = cu.update_model(
        models.Corporate,
        corporate,
        {"uuid": db_corporate.uuid},
    )

    cu.db.commit()
    cu.db.refresh(db_corporate)

    return db_corporate


def delete_corporate(
    cu: CrudUtil,
    uuid: str,
) -> dict[str, Any]:

    db_corporate: models.Corporate = cu.get_model_or_404(
        models.Corporate,
        {"uuid": uuid},
    )

    try:
        db_corporate.user.groups.remove(get_group_by_name(cu, "corporate_user_group"))
    except ValueError:
        pass

    # now delete the profile
    cu.delete_model(
        models.Corporate,
        {"uuid": uuid},
    )

    return delete_user(
        cu,
        str(db_corporate.user.uuid),
        autocommit=True
    )


def search_corporate(
    cu: CrudUtil,
    search: schemas.CorporateSearch,
) -> Any:
    return cu.search_model(
        models.Corporate,
        search.search,
        search.search_fields,
        join_search=search.join_search,
        skip=search.skip,
        limit=search.limit,
        order=search.order,
    )


# ====================[ Subject ]====================

def create_subject(
    cu: CrudUtil,
    subject_data: schemas.SubjectCreate
) -> models.Subject:
    subject: models.Subject = cu.create_model(models.Subject, subject_data)
    return subject


def get_subject_by_uuid(
    cu: CrudUtil,
    uuid: str
) -> models.Subject:
    subject: models.Subject = cu.get_model_or_404(
        models.Subject,
        {"uuid": uuid}
    )
    return subject


def update_subject(
    cu: CrudUtil,
    uuid: str,
    update_data: schemas.SubjectUpdate,
) -> models.Subject:
    subject: models.Subject = cu.update_model(
        model_to_update=models.Subject,
        update=update_data,
        update_conditions={"uuid": uuid}
    )
    return subject


def list_subject(
    cu: CrudUtil,
    skip: int,
    limit: int,
) -> schemas.SubjectList:
    subjects: dict[str, Any] = cu.list_model(
        model_to_list=models.Subject,
        skip=skip,
        limit=limit
    )
    return schemas.SubjectList(**subjects)


def delete_subject(
    cu: CrudUtil,
    uuid: str,
) -> dict[str, Any]:
    return cu.delete_model(
        model_to_delete=models.Subject,
        delete_conditions={"uuid": uuid}
    )


# ====================[ Framework ]====================

def create_framework(
    cu: CrudUtil,
    framework_data: schemas.FrameworkCreate
) -> models.Framework:
    cu.ensure_unique_model(models.Framework, {"name": framework_data.name})
    framework: models.Framework = cu.create_model(models.Framework, framework_data)
    return framework


def get_framework_by_uuid(
    cu: CrudUtil,
    uuid: str
) -> models.Framework:
    framework: models.Framework = cu.get_model_or_404(
        models.Framework,
        {"uuid": uuid}
    )
    return framework


def update_framework(
    cu: CrudUtil,
    uuid: str,
    update_data: schemas.FrameworkUpdate,
) -> models.Framework:
    framework: models.Framework = cu.update_model(
        model_to_update=models.Framework,
        update=update_data,
        update_conditions={"uuid": uuid}
    )
    return framework


def list_framework(
    cu: CrudUtil,
    skip: int,
    limit: int,
) -> schemas.FrameworkList:
    framework: dict[str, Any] = cu.list_model(
        model_to_list=models.Framework,
        skip=skip,
        limit=limit
    )
    return schemas.FrameworkList(**framework)


def delete_framework(
    cu: CrudUtil,
    uuid: str,
) -> dict[str, Any]:
    return cu.delete_model(
        model_to_delete=models.Framework,
        delete_conditions={"uuid": uuid}
    )


# ====================[ Class ]====================


def create_class(
    cu: CrudUtil,
    class_data: schemas.ClassCreate
) -> models.Class:
    cu.ensure_unique_model(
        model_to_check=models.Class,
        unique_condition={"name": class_data.name}
    )

    new_class: models.Class = cu.create_model(
        model_to_create=models.Class,
        create=class_data
    )

    return new_class

def get_class_by_uuid(
    cu: CrudUtil,
    uuid: str,
) -> models.Class:

    db_class: models.Class = cu.get_model_or_404(
        model_to_get=models.Class,
        model_conditions={"uuid": uuid}
    )
    return db_class


def  update_class(
    cu: CrudUtil,
    uuid: str,
    update_data: schemas.ClassUpdate,
) -> models.Class:
    db_class: models.Class = cu.update_model(
        model_to_update=models.Class,
        update=update_data,
        update_conditions={"uuid": uuid},
        autocommit=False if update_data.subjects else True,
    )

    if update_data.subjects:
        for subject_uuid in update_data.subjects:
            db_class.subjects.append(
                get_subject_by_uuid(cu, uuid=subject_uuid)
            )

    cu.db.commit()
    cu.db.refresh(db_class)

    return db_class


def list_class(cu: CrudUtil, skip: int, limit: int) -> schemas.ClassList:
    roles: dict[str, Any] = cu.list_model(
        model_to_list=models.Class,
        skip=skip,
        limit=limit
    )

    return schemas.ClassList(**roles)


def delete_class(cu: CrudUtil, uuid: str) -> dict[str, Any]:
    return cu.delete_model(
        model_to_delete=models.Class,
        delete_conditions={"uuid": uuid}
    )


# ====================[ Subscription ]====================

def create_subscription(
    cu: CrudUtil,
    subscription: schemas.SubscriptionIn
) -> schemas.SubscriptionOut | models.Subscription:
    db_subscription: models.Subscription = cu.create_model(
        models.Subscription,
        subscription
    )

    return db_subscription


def get_subscription_by_uuid(
    cu: CrudUtil,
    uuid: str,
) -> models.Subscription:
    subscription: models.Subscription = cu.get_model_or_404(
        models.Subscription,
        {"uuid": uuid}
    )
    return subscription


def list_subscription(
    cu: CrudUtil,
    filter: schemas.SubscriptionFilter
) -> Any:
    # Get the current date and time
    current_datetime = datetime.now()

    return cu.list_model(
        models.Subscription,
        filter.model_dump(exclude_unset=True)
    )


def update_subscription(
    cu: CrudUtil,
    uuid: str,
    update_data: schemas.SubscriptionUpdate,
) -> models.Subscription:
    subscription: models.Subscription = cu.update_model(
        model_to_update=models.Subscription,
        update=update_data,
        update_conditions={"uuid": uuid}
    )
    if update_data.subjects:
        subscription.subjects = get_subject_by_uuid(cu, uuid=update_data.subjects)
    if update_data.framework:
        subscription.framework = get_framework_by_uuid(cu, uuid=update_data.framework)

    cu.db.commit()
    cu.db.refresh(subscription)

    return subscription


def search_subscription(
    cu: CrudUtil,
    search: schemas.SubscriptionSearch
) -> Any:
    return cu.search_model(
        models.Subscription,
        search.search,
        search.search_fields,
        skip=search.skip,
        limit=search.limit,
        order=search.order
    )


def delete_subscription(
    cu: CrudUtil,
    uuid: str,
) -> dict[str, Any]:
    return cu.delete_model(
        model_to_delete=models.Subscription,
        delete_conditions={"uuid": uuid}
    )


# ====================[ Subscription Plan ]====================

def create_subscription_plan(
    cu: CrudUtil,
    plan: schemas.SubscriptionPlanIn
) -> schemas.SubscriptionPlanOut | models.SubscriptionPlan:
    new_plan: models.SubscriptionPlan = cu.create_model(
        models.SubscriptionPlan,
        plan
    )
    return new_plan


def get_subscription_plan_by_uuid(
    cu: CrudUtil,
    uuid: str
) -> schemas.SubscriptionPlanOut:
    plan: models.SubscriptionPlan = cu.get_model_or_404(
        models.SubscriptionPlan,
        {"uuid": uuid}
    )
    return plan


def list_subscription_plans(
    cu: CrudUtil,
    filter: schemas.SubscriptionPlanFilter
) -> Any:
    return cu.list_model(
        models.SubscriptionPlan,
        filter.model_dump(exclude_unset=True)
    )


def update_subscription_plan(
    cu: CrudUtil,
    uuid: str,
    update_plan: schemas.SubscriptionPlanUpdate
) -> models.SubscriptionPlan:
    plan: models.SubscriptionPlan = cu.update_model(
        model_to_update=models.SubscriptionPlan,
        update=update_plan,
        update_conditions={"uuid": uuid}
    )

    if update_plan.subscription:
        plan.subscription = get_subscription_by_uuid(cu, uuid=update_plan.subscription)

    cu.db.commit()
    cu.db.refresh(plan)

    return plan


def delete_subscription_plan(
    cu: CrudUtil,
    uuid: str
) -> dict[str, Any]:
    return cu.delete_model(
        model_to_delete=models.SubscriptionPlan,
        delete_conditions={"uuid": uuid}
    )


# ====================[ User Subscription ]====================

def create_user_subscription(
    cu: CrudUtil,
    subscription: schemas.UserSubscriptionIn,
) -> schemas.UserSubscriptionOut | models.UserSubscription:
    new_subscription: models.UserSubscription = cu.create_model(
        models.UserSubscription,
        subscription
    )
    return new_subscription


def get_user_subscription_by_uuid(
    cu: CrudUtil,
    uuid: str
) -> schemas.UserSubscriptionOut:
    subscription: models.UserSubscription = cu.get_model_or_404(
        models.UserSubscription,
        {"uuid": uuid}
    )
    return subscription


def list_user_subscription(
    cu: CrudUtil,
    filter: schemas.UserSubscriptionFilter
) -> Any:
    current_date = date.today()
    from_date = current_date - timedelta(days=365)
    to_date = current_date
    date_range = DateRange(
        column_name='end_date', 
        from_date=from_date, 
        to_date=to_date
    )
    return cu.list_model(
        models.UserSubscription,
        filter.model_dump(exclude_unset=True),
        date_range=date_range,
    )