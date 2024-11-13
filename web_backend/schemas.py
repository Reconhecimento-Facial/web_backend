from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from web_backend.models import UserStatus


class MessageSchema(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublicSchema(BaseModel):
    id: int
    username: str
    status: UserStatus
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserDbSchema(UserSchema):
    id: int
