from app.mixins.schemas import (
    BaseModelIn,
    BaseModelCreate,
    BaseModelFilter,
    BaseModelMin,
    BaseModelSearch,
    BaseModelOut,
    JoinSearch,
)
from app.user.models import User
from app.user.schemas import UserIn, UserUpdate, UserUpdateSelf
from app.utils.custom_validators import CapStr, UpStr
from app.utils.enums import Gender
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
    ValidationInfo,
    computed_field,
    Field,
    field_validator,
)


class ProfileIn(BaseModelIn):
    user: UserIn
    state_id: str | None = None
    lga_id: str | None = None
    address: UpStr | None = None
    date_of_birth: UpStr | None = None
    gender: Gender | None = None


class ProfileCreate(BaseModelCreate):
    user_id: str
    state_id: str | None = None
    lga_id: str | None = None
    address: UpStr | None = None
    date_of_birth: UpStr | None = None
    gender: Gender | None = None


class ProfileUpdate(BaseModelIn):
    user: UserUpdate | None = Field(None, exclude=True)
    state_id: str | None = None
    lga_id: str | None = None
    address: UpStr | None = None
    date_of_birth: UpStr | None = None
    gender: Gender | None = None


class ProfileFilter(BaseModelFilter):
    state_id: str | None = None
    lga_id: str | None = None
    gender: Gender | None = None