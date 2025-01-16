from datetime import date
from enum import Enum
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, EmailStr, Field

from web_backend.models.user import UserStatus

from .message import Message
from .schemas_utils import form_body_user_schema, form_body_user_schema_put


@form_body_user_schema
class UserSchema(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: date
    cpf: str
    phone_number: str


@form_body_user_schema_put
class UserSchemaPut(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: date
    cpf: str
    phone_number: str
    status: str


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


class UserPublicWithUrl(UserPublic):
    photo_url: str


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


class UserFilter(BaseModel):
    class SortByOptions(str, Enum):
        name_opt = 'name'
        email_opt = 'email'

    class AscendingOrDescending(str, Enum):
        ascending = 'ascending'
        descending = 'descending'

    name: Annotated[
        str | None, Query(None, description='Filter by user name')
    ] = None
    status: Annotated[
        UserStatus | None, Query(None, description='Filter by user status')
    ] = None
    sort_by: Annotated[
        SortByOptions | None, Query(None, description='Sort the result')
    ] = None
    sort_order: Annotated[
        AscendingOrDescending | None,
        Query(None, description='Sort in ascending or descending order'),
    ]
