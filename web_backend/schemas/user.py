from datetime import date
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from web_backend.models.user import UserStatus

from .message import Message
from .schemas_utils import form_body_user_schema


@form_body_user_schema
class UserSchema(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: date
    cpf: str
    phone_number: str


class UserPatch(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    date_of_birth: date | None = None
    cpf: Annotated[
        str | None, Field(pattern=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
    ] = None
    phone_number: Annotated[
        str | None, Field(pattern=r'^\(\d{2}\) 9\d{4}-\d{4}$')
    ] = None
    status: UserStatus | None = None


class UserPublic(UserSchema):
    id: int
    status: UserStatus

    class Config:
        from_attributes = True


class UserCreated(Message):
    user_created: UserPublic
    photo: str
    environments_ids: list[int]
    invalid_environments_ids: list[int]


class UserUpdated(Message):
    user_updated: UserPublic


class ExistingUser(Message):
    existing_user: UserPublic


class UserNameId(BaseModel):
    id: int
    name: str