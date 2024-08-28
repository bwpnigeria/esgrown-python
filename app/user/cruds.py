from typing import Any
from fastapi import HTTPException

from app.user import schemas, models
from app.utils.crud_util import CrudUtil
from app.utils.mail import (
    send_change_password_mail,
    send_account_create_mail,
)
from app.utils.misc import gen_random_password
from app.utils.sms import send_account_creation_sms, send_password_change_sms
from app.utils.user import get_password_hash, verify_password


def create_user(
    cu: CrudUtil,
    user_data: schemas.UserIn,
    autocommit: bool = True,
    is_admin: bool = False,
    can_login: bool = True,
) -> models.User:
    # password and hash generated
    # in class using validators
    user_to_create = schemas.UserCreate(
        **user_data.model_dump(),
        password="",
        password_hash="",
        is_admin=is_admin,
        can_login=can_login,
    )

    cu.ensure_unique_model(
        model_to_check=models.User, unique_condition={"email": user_data.email}
    )

    user: models.User = cu.create_model(
        model_to_create=models.User, create=user_to_create, autocommit=autocommit
    )

    if is_admin or can_login:
        send_account_create_mail(
            str(user.email), user_to_create.password, str(user.firstname)
        )

    return user


def create_user_account(
    cu: CrudUtil,
    user_data: schemas.UserAccountIn,
    autocommit: bool = True,
    is_admin: bool = False,
    can_login: bool = True,
) -> models.User:
    # password and hash generated in class using validators
    user_data.password = get_password_hash(user_data.password)
    
    user_to_create = schemas.UserAccountCreate(
        **user_data.model_dump(),
        is_admin=is_admin,
        can_login=can_login,
        password_hash=user_data.password,
        temp_password_hash=user_data.password
    )

    cu.ensure_unique_model(
        model_to_check=models.User, unique_condition={"email": user_data.email}
    )

    user: models.User = cu.create_model(
        model_to_create=models.User, create=user_to_create, autocommit=autocommit
    )

    return user



def activate_user(
    cu: CrudUtil,
    uuid: str,
    autocommit: bool = True,
    send_mail: bool = False,
    send_sms: bool = False,
) -> models.User:
    db_user = get_user_by_uuid(cu, uuid)
    user_active = schemas.UserActivate(password="", password_hash="")

    db_user.can_login = user_active.can_login  # type: ignore
    db_user.temp_password_hash = user_active.password_hash  # type: ignore
    if send_mail:
        send_account_create_mail(
            str(db_user.email), user_active.password, str(db_user.firstname)
        )

    if send_sms:
        send_account_creation_sms(
            str(db_user.phone),
            str(db_user.phone),
            user_active.password,
            str(db_user.firstname),
        )

    if autocommit:
        cu.db.commit()
        cu.db.refresh(db_user)

    return db_user


def get_user_by_email(cu: CrudUtil, email: str) -> models.User:
    user: models.User = cu.get_model_or_404(
        model_to_get=models.User, model_conditions={"email": email}
    )

    return user


def get_user_by_phone(cu: CrudUtil, phone: str) -> models.User:
    user: models.User = cu.get_model_or_404(
        model_to_get=models.User, model_conditions={"phone": phone}
    )

    return user


def get_super_admin(cu: CrudUtil) -> models.User:
    user: models.User | None = (
        cu.db.query(models.User).filter(models.User.is_admin == True).first()  # noqa
    )

    if not user:
        raise HTTPException(status_code=404, detail="Super admin not found")

    return user


def get_user_by_uuid(
    cu: CrudUtil,
    uuid: str,
) -> models.User | schemas.UserSchema:
    user: models.User = cu.get_model_or_404(
        model_to_get=models.User, model_conditions={"uuid": uuid}
    )
    return user


def update_user(
    cu: CrudUtil,
    uuid: str,
    user_data: schemas.UserUpdate | schemas.UserUpdateSelf,
    autocommit: bool = True,
) -> models.User:
    user: models.User = cu.update_model(
        model_to_update=models.User,
        update=user_data,
        update_conditions={"uuid": uuid},
        autocommit=autocommit,
    )

    return user


def delete_user(cu: CrudUtil, uuid: str, autocommit: bool = True) -> dict[str, Any]:
    return cu.delete_model(
        model_to_delete=models.User,
        delete_conditions={"uuid": uuid},
        autocommit=autocommit,
    )


def authenticate_user(
    cu: CrudUtil,
    email_or_phone: str,
    password: str,
) -> schemas.UserSchema:
    try:
        user: models.User = get_user_by_email(cu, email_or_phone)
    except HTTPException as e:
        if e.status_code == 404:
            try:
                user = get_user_by_phone(cu, email_or_phone)
            except HTTPException:
                raise HTTPException(
                    status_code=400, detail="Email and password do not match"
                )

    if not user.is_active or not user.can_login:  # type: ignore
        raise HTTPException(status_code=400, detail="Email and password do not match")

    if not verify_password(password, str(user.password_hash)):
        # check whether it's a temp password
        temp_password = str(user.temp_password_hash)
        if temp_password == "None":
            raise HTTPException(
                status_code=400, detail="Email and password do not match"
            )

        if temp_password and verify_password(password, temp_password):
            user.password_hash = temp_password  # type: ignore
            user.temp_password_hash = ""  # type: ignore
            cu.db.commit()
            return schemas.UserSchema.model_validate(user)
        raise HTTPException(status_code=400, detail="Email and password do not match")

    return schemas.UserSchema.model_validate(user)


def reset_password(
    cu: CrudUtil,
    email_or_phone: str,
) -> dict[str, Any]:
    # first try to get user by email
    is_email = False
    is_phone = False
    try:
        user = get_user_by_email(cu, email_or_phone)
        is_email = True
    except HTTPException as e:
        try:
            if e.status_code == 404:
                user = get_user_by_phone(cu, email_or_phone)
                is_phone = True
        except Exception:
            return {
                "detail": "Your password has been sent to your email or phone if it exists on the system. "
            }
    except Exception:
        return {
            "detail": "Your password has been sent to your email or phone if it exists on the system. "
        }

    new_password = gen_random_password()
    new_password_hash = get_password_hash(new_password)
    user.temp_password_hash = new_password_hash  # type: ignore
    cu.db.commit()

    if is_email:
        send_change_password_mail(str(user.email), new_password)
    elif is_phone:
        send_password_change_sms(
            str(user.phone), str(user.phone), new_password, str(user.firstname)
        )
    return {
        "detail": "Your password has been sent to your email or phone if it exists on the system. "
    }


def list_admin_users(
    cu: CrudUtil, filter_: schemas.AdminUserFilter, skip: int = 0, limit: int = 100
) -> schemas.UserList:
    conditions = filter_.model_dump(exclude_unset=True, exclude={"user_group_name"})
    conditions["is_admin"] = True

    db_result: dict[str, Any] = cu.list_model(
        model_to_list=models.User,
        list_conditions=conditions,
        skip=skip,
        limit=limit,
    )

    if filter_.user_group_name:

        def filter_user_group(user: models.User) -> bool | Any:
            if user.groups:
                return user.groups[0].name == filter_.user_group_name

            return False

        db_result["items"] = list(filter(filter_user_group, db_result["items"]))
        return schemas.UserList(**db_result)

    return schemas.UserList(**db_result)


def change_admin_password(
    cu: CrudUtil,
    user_uuid: str,
) -> schemas.PasswordChangeOut:
    db_user: models.User = cu.get_model_or_404(
        model_to_get=models.User, model_conditions={"uuid": user_uuid}
    )
    password = gen_random_password()
    hashed_password = get_password_hash(password)

    db_user.temp_password_hash = hashed_password  # type: ignore
    cu.db.commit()
    send_change_password_mail(str(db_user.email), password)
    return schemas.PasswordChangeOut(password=password)


def change_own_password(
    cu: CrudUtil,
    user: schemas.UserSchema,
) -> schemas.PasswordChangeOut:
    db_user: models.User = cu.get_model_or_404(
        model_to_get=models.User, model_conditions={"uuid": user.uuid}
    )
    password = gen_random_password()
    hashed_password = get_password_hash(password)

    db_user.temp_password_hash = hashed_password  # type: ignore
    cu.db.commit()
    send_change_password_mail(str(db_user.email), password)
    return schemas.PasswordChangeOut(password=password)
