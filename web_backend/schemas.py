from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from web_backend.models import WorkerStatus


class MessageSchema(BaseModel):
    message: str


class WorkerSchema(BaseModel):
    name: str
    email: EmailStr
    status: WorkerStatus = Field(default=WorkerStatus.disabled)
    model_config = ConfigDict(from_attributes=True)


class WorkerDbSchema(WorkerSchema):
    id: int


class WorkerPublicSchema(BaseModel):
    id: int
    name: str
    status: WorkerStatus
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class WorkersListSchema(BaseModel):
    users: list[WorkerPublicSchema]


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None
