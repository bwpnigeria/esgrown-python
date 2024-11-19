#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2024-08-26 15:30
# @Author  : Nasir Lawal (nasirlawal001@gmail.com)
# @Link    : link
# @Version : 1.0.0


from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from typing import Any
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, Request
from app.user.schemas import UserSchema
from app.config.config import settings
import requests
from app.profile import schemas, cruds, models
from app.utils.crud_util import CrudUtil
from app.dependencies.dependencies import (
    HasPermission,
    get_current_user,
)
from decimal import Decimal

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

subscription_router = APIRouter(
    prefix="/subscription",
    tags=["Subscription Routes"],
)

subscription_plan_router = APIRouter(
    prefix="/subscription_plan",
    tags=["Subscription Plan Routes"]
)

user_subscriptoin_router = APIRouter(
    prefix="/user-subscription",
    tags=["User Subscription Routes"]
)

framework_router = APIRouter(
    prefix="/framework",
    tags=["Framework Routes"],
)

payment_router = APIRouter(
    prefix="/payment",
    tags=["Payment Routes"]
)

discount_router = APIRouter(
    prefix="/discount",
    tags=["Discount Routes"]
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
def delete_corporate(
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


# ================ Framework ================

@framework_router.post(
    "",
    dependencies=[Depends(HasPermission(["framework:create"]))],
)
async def create_framework(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    framework_data: schemas.FrameworkCreate
) -> schemas.FrameworkSchema:
    return cruds.create_framework(cu, framework_data)


@framework_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["framework:read"]))],
)
def framework_detail(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> schemas.FrameworkSchema:
    return cruds.get_framework_by_uuid(cu, uuid)


@framework_router.put(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["framework:update"]))],
)
def update_framework(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    framework_data: schemas.FrameworkUpdate,
) -> schemas.FrameworkSchema:
    return cruds.update_framework(cu, uuid, framework_data)


@framework_router.get(
    "",
    dependencies=[Depends(HasPermission(["framework:list"]))],
)
def framework_list(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    skip: int = 0,
    limit: int = 100,
) -> schemas.FrameworkList:
    return cruds.list_framework(cu, skip, limit)


@framework_router.delete(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["framework:delete"]))],
)
def delete_framework(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> dict[str, Any]:
    return cruds.delete_framework(cu, uuid)



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


# ================ Subscription ================


@subscription_router.post(
    "",
    dependencies=[Depends(HasPermission(["subscription:create"]))],
)
async def create_subscription(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    subscription: schemas.SubscriptionIn
) -> schemas.SubscriptionOut:
    return cruds.create_subscription(cu, subscription)


@subscription_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["subscription:read"]))],
)
def subscription_detail(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
) -> schemas.SubscriptionOut:
    return cruds.get_subscription_by_uuid(cu, uuid)


@subscription_router.get(
    "",
    dependencies=[Depends(HasPermission(["subscription:list"]))],
    response_model=schemas.SubscriptionList,
)
async def subscription_list(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    filter: schemas.SubscriptionFilter = Depends(),
) -> Any:
    return cruds.list_subscription(cu, filter)


@subscription_router.put(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["subscription:update"]))],
)
def update_subscription(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    update_data: schemas.SubscriptionUpdate,
) -> schemas.SubscriptionOut:
    return cruds.update_subscription(cu, uuid, update_data)


@subscription_router.get(
    "/search/all/subscription",
    dependencies=[Depends(HasPermission(["subscription:search"]))],
    response_model=schemas.SubscriptionList,
)
async def search_subscription(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    search: schemas.SubscriptionSearch = Depends()
) -> Any:
    return cruds.search_subscription(cu, search)


@subscription_router.delete(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["subscription:delete"]))],
)
def delete_subscription(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str
) -> dict[str, Any]:
    return cruds.delete_subscription(cu, uuid)


# ======================[ Subscription Plan ]=======================

@subscription_plan_router.post(
    "",
    dependencies=[Depends(HasPermission(["subscription_plan:create"]))]
)
async def create_subscription_plan(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    plan: schemas.SubscriptionPlanIn
) -> schemas.SubscriptionPlanOut:
    return cruds.create_subscription_plan(cu, plan)


@subscription_plan_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["subscription_plan:read"]))],
)
def subscription_plan_detail(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str
) -> schemas.SubscriptionPlanOut:
    return cruds.get_subscription_plan_by_uuid(cu, uuid)


@subscription_plan_router.get(
    "",
    dependencies=[Depends(HasPermission(["subscription_plan:list"]))],
    response_model=schemas.SubscriptionPlanList
)
def subscription_plan_list(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    filter: schemas.SubscriptionPlanFilter = Depends()
) -> Any:
    return cruds.list_subscription_plans(cu, filter)


@subscription_plan_router.put(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["subscription_plan:update"]))],
)
def update_subscription_plan(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str,
    update_plan: schemas.SubscriptionPlanUpdate
) -> schemas.SubscriptionPlanOut:
    return cruds.update_subscription_plan(cu, uuid, update_plan)


@subscription_plan_router.delete(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["subscription_plan:delete"]))]
)
def delete_subscription_plan(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str
) -> dict[str, Any]:
    return cruds.delete_subscription_plan(cu, uuid)


# ======================[ User Subscription ]=======================

@user_subscriptoin_router.post(
    "",
    dependencies=[Depends(HasPermission(["user_subscription:create"]))]
)
async def create_user_subscription(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    subscription: schemas.UserSubscriptionIn,
) -> schemas.UserSubscriptionOut:
    return cruds.create_user_subscription(cu, subscription)


@user_subscriptoin_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["user_subscription:read"]))]
)
def user_subscription_detail(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str
) -> schemas.UserSubscriptionOut:
    return cruds.get_user_subscription_by_uuid(cu, uuid)


@user_subscriptoin_router.get(
    "",
    dependencies=[Depends(HasPermission(["subscription_plan:list"]))],
    response_model=schemas.UserSubscriptionList
)
def user_subscription_list(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    filter: schemas.UserSubscriptionFilter = Depends(),
) -> Any:
    return cruds.list_user_subscription(cu, filter)


# ======================[ payment ]=======================

@payment_router.post("/create-payment-url")
async def create_paystack_payment_url(
    uuid: str,
    coupon_code: str = None,
    user: UserSchema = Depends(get_current_user),
    cu: CrudUtil = Depends(CrudUtil),
):
    headers = {
        "Authorization": f"Bearer {settings.paystack_secret_key}",
        "Content-Type": "application/json"
    }

    subscription = cruds.get_subscription_plan_by_uuid(cu, uuid)
    if not subscription:
        raise HTTPException(status_code=400, detail="Unable to create Paystack payment URL")
    
    if coupon_code:
        discount = cruds.get_discount_by_name(cu, name=coupon_code)
        if not discount:
            raise HTTPException(status_code=400, detail="Invalid coupon code")
        
        try:
            discount_percentage = Decimal(str(discount.percentage))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid discount percentage value")
        
        discount_amount = (subscription.price * discount_percentage) / 100
        amount = int((subscription.price - discount_amount) * 100)
    else:
        amount = int(subscription.price * 100)

    payload = {
        "email": user.email,
        "amount": amount
    }

    response = requests.post(
        settings.paystack_payment_url,
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Unable to create Paystack payment URL")

    response_data = response.json()
    print(response_data)
    
    if not response_data.get("status"):
        raise HTTPException(status_code=400, detail="Failed to initialize Paystack payment")
    
    payment_url = response_data["data"]["authorization_url"]

    return {"payment_url": payment_url}


@payment_router.get("/thirdparty-payment-verify")
async def verify_paystack_payment(
    reference: str,
    plan_uuid: str,
    user: UserSchema = Depends(get_current_user),
    cu: CrudUtil = Depends(CrudUtil),
):
    headers = {
        "Authorization": f"Bearer {settings.paystack_secret_key}",
        "Content-Type": "application/json",
    }

    verification_url = f"{settings.paystack_verify_url}/{reference}"
    response = requests.get(verification_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to verify payment")

    response_data = response.json()

    if not response_data.get("status") or response_data["data"]["status"] != "success":
        raise HTTPException(status_code=400, detail="Payment verification failed")
    
    subscription_plan = cruds.get_subscription_plan_by_uuid(cu, plan_uuid)
    if not subscription_plan:
        raise HTTPException(status_code=400, detail="Payment verification failed")

    if int(response_data["data"]['requested_amount']) != (subscription_plan.price * 100):
        raise HTTPException(status_code=400, detail="Payment verification failed")
    
    # Determine start and end dates based on plan duration
    start_date = datetime.now(timezone.utc).date()
    
    # Calculate end date based on subscription plan duration
    duration = subscription_plan.duration.lower()

    match duration:
        case "monthly":
            end_date = start_date + relativedelta(months=1)
        case "quarterly":
            end_date = start_date + relativedelta(months=3)
        case "biannual":
            end_date = start_date + relativedelta(months=6)
        case "annually":
            end_date = start_date + relativedelta(years=1)
        case _:
            raise HTTPException(status_code=400, detail="Invalid subscription duration")

    # Attempt to fetch the individual profile
    try:
        individual = cruds.get_own_profile(cu, user)
    except Exception as e:
        pass
    # Attempt to fetch the corporate profile
    try:
        corporate = cruds.get_own_corporate(cu, user)
    except Exception as e:
        pass

    account_type = ''
    if individual:
        account_type = 'individual'
    elif corporate:
        account_type = 'corporate'

    individual_id = individual.uuid if account_type == 'individual' else None
    corporate_id = corporate.uuid if account_type == 'corporate' else None

    subscription_data = schemas.UserSubscriptionIn(
        individual_id=individual_id,
        corporate_id=corporate_id,
        subscription_plan_id=subscription_plan.uuid,
        start_date=start_date,
        end_date=end_date
    )

    user_subscription = cruds.create_user_subscription(cu, subscription_data)
    
    return {
        "message": "Payment verified successfully",
        "payment_details": response_data["data"],
        "user_subscription": user_subscription
    }


# ======================[ Discount ]=======================

@discount_router.post(
    "",
    dependencies=[Depends(HasPermission(["discount:create"]))]
)
async def create_discount(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    discount: schemas.DiscountIn,
) -> schemas.DiscountOut:
    return cruds.create_discount(cu, discount)


@discount_router.get(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["discount:read"]))]
)
def discount_detail(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str
) -> schemas.DiscountOut:
    return cruds.get_discount_by_uuid(cu, uuid)

@discount_router.get(
    "/name/{name}",
    dependencies=[Depends(HasPermission(["discount:read"]))]
)
def discount_detail_by_name(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    name: str
) -> schemas.DiscountOut:
    return cruds.get_discount_by_name(cu, name)


@discount_router.get(
    "",
    dependencies=[Depends(HasPermission(["discount:list"]))],
    response_model=schemas.DiscountList
)
def discount_list(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    skip: int = 0,
    limit: int = 100,
) -> schemas.DiscountList:
    return cruds.list_discount(cu, skip, limit)


@discount_router.put(
    '/{uuid}',
    dependencies=[Depends(HasPermission(["discount:update"]))],
)
def update_discount(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    discount_data: schemas.UpdateDiscount,
    uuid: str
) -> schemas.DiscountOut:
    return cruds.update_discount(cu, uuid, discount_data)


@discount_router.delete(
    "/{uuid}",
    dependencies=[Depends(HasPermission(["discount:delete"]))]
)
def delete_discount(
    *,
    cu: CrudUtil = Depends(CrudUtil),
    uuid: str
) -> dict[str, Any]:
    return cruds.delete_discount(cu, uuid)


# {
#   "name": "TEST3000",
#   "percentage": 20,
#   "plans": [
#     "01JBSSQ3SBB41P8QXYQMTJVEZC"
#   ],
#   "countries": [
#     "01JBSS68TPE86025MT1APF5QDH"
#   ],
#   "states": [
#     "01JBSS6QYJ894X4Y69Q96CW0FH"
#   ],
#   "cities": null
# }