# from logfire.integrations.pydantic import PluginSettings
from typing import List, Optional
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ValidationInfo,
    computed_field,
    field_validator,
)

from app.mixins.commons import ListBase

from app.mixins.schemas import BaseModelPublic, BaseSchemaMixin
from app.access_control.schemas import GroupSchema, GroupOutSchema
from app.utils.custom_validators import UpStr
from app.utils.misc import gen_email, gen_random_password, gen_random_phone
from app.utils.user import get_password_hash


class UserIn(BaseModel):
    email: EmailStr | None = Field(
        default_factory=gen_email, description="Email address of the user"
    )
    firstname: UpStr
    lastname: UpStr
    middlename: UpStr | None = None
    phone: str | None = Field(
        default_factory=gen_random_phone, description="Phone number of the user"
    )


class UserAccountIn(BaseModel):
    email: EmailStr | None = Field(
        default_factory=gen_email, description="Email address of the user"
    )
    firstname: UpStr
    lastname: UpStr
    middlename: UpStr | None = None
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    temp_password_hash: str = ""
    password: str
    password_hash: str
    firstname: str
    lastname: str
    middlename: Optional[str]
    is_admin: bool
    can_login: bool = True
    phone: str | None = None

    @field_validator("password")
    @classmethod
    def _gen_password(cls, val: str) -> str:
        return gen_random_password()

    @field_validator("password_hash")
    @classmethod
    def _hash_password(cls, val: str, info: ValidationInfo) -> str:
        return get_password_hash(info.data["password"])

    @computed_field
    @property
    def is_temp_email(self) -> bool:
        return self.email.endswith("@alumnimail.com")

    @computed_field
    @property
    def is_temp_phone(self) -> bool:
        return self.phone.startswith("4134") if self.phone else False

    @computed_field
    @property
    def fullname(self) -> str:
        return f"{self.firstname} {self.middlename if self.middlename else ''} {self.lastname}".strip()
    

class UserAccountCreate(BaseModel):
    email: EmailStr
    password: str
    temp_password_hash: str = ""
    password_hash: str = ""
    firstname: str
    lastname: str
    middlename: Optional[str]
    is_admin: bool
    can_login: bool = True
    phone: str | None = None

    @computed_field
    @property
    def fullname(self) -> str:
        return f"{self.firstname} {self.middlename if self.middlename else ''} {self.lastname}".strip()


class UserGroup(BaseModel):
    groups: List[str]


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    firstname: UpStr | None = None
    lastname: UpStr | None = None
    middlename: UpStr | None = None
    is_active: bool | None = None
    phone: str | None = None


class UserUpdateSelf(BaseModel):
    firstname: UpStr | None = None
    lastname: UpStr | None = None
    middlename: UpStr | None = None


class UserActivate(BaseModel):
    password: str
    password_hash: str
    can_login: bool = True

    @field_validator("password")
    @classmethod
    def _gen_password(cls, val: str) -> str:
        return gen_random_password()

    @field_validator("password_hash")
    @classmethod
    def _hash_password(cls, val: str, info: ValidationInfo) -> str:
        return get_password_hash(info.data["password"])


class AdminUserFilter(BaseModel):
    email: EmailStr | None = None
    firstname: UpStr | None = None
    lastname: UpStr | None = None
    middlename: UpStr | None = None
    user_group_name: str | None = None
    is_active: bool | None = None
    phone: str | None = None


class ChangePasswordFromDashboard(BaseModel):
    current_password: str
    new_password: str


class UserSchema(BaseSchemaMixin):
    email: EmailStr
    firstname: UpStr
    lastname: UpStr
    middlename: UpStr | None = ""
    is_active: bool
    is_admin: bool
    phone: str | None = None
    groups: list[GroupSchema]

    @property
    def permissions(self) -> List[str]:
        perms: list[str] = []
        for group in self.groups:
            for role in group.roles:
                for perm in role.permissions:
                    perms.append(perm.name)
        return list(set(perms))

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions


class UserOut(BaseSchemaMixin):
    email: EmailStr
    firstname: UpStr
    lastname: UpStr
    middlename: Optional[UpStr] = ""
    is_active: bool
    is_admin: bool
    groups: List[GroupOutSchema]


class UserPublic(BaseModelPublic):
    firstname: UpStr
    lastname: UpStr
    middlename: Optional[UpStr] = ""


class UserList(ListBase):
    items: list[UserOut]


class ResetPassword(BaseModel):
    password: str


class PasswordChangeOut(BaseModel):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    permissions: list[str] | None = None


class UserToken(BaseModel):
    access_token: str
    token_type: str


class Login(BaseModel):
    email_or_phone: str = Field(
        description="Email address or phone number of the user",
        pattern="^[0-9a-zA-Z@.]+$",
    )
    password: str
