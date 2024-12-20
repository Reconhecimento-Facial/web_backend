from datetime import date

from fastapi import Form
from pydantic import BaseModel, EmailStr

from .message import Message


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


@form_body
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
    cpf: str | None = None
    phone_number: str | None = None


class UserPublic(UserSchema):
    id: int


class UserCreated(Message):
    user_created: UserPublic
    photo: str


class UserUpdated(Message):
    user_updated: UserPublic


class ExistingUser(Message):
    existing_user: UserPublic


class UserNameId(BaseModel):
    id: int
    name: str
