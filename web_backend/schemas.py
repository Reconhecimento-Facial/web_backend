from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from web_backend.models import UserStatus


class MessageSchema(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    status: UserStatus = Field(default=UserStatus.disabled)
    model_config = ConfigDict(from_attributes=True)


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


class UsersListSchema(BaseModel):
    users: list[UserPublicSchema]


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None
