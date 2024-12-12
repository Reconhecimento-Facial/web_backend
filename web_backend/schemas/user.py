from datetime import date

from pydantic import BaseModel, EmailStr

from .message import Message


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


class UserUpdated(Message):
    user_updated: UserPublic


class ExistingUser(Message):
    existing_user: UserPublic
