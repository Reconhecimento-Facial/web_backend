from datetime import datetime

from pydantic import BaseModel

from .message import Message


class EnvironmentSchema(BaseModel):
    name: str


class EnvironmentPublic(EnvironmentSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    creator_admin_id: int


class Environments(BaseModel):
    environments: list[EnvironmentPublic]


class EnvironmentUpdated(Message):
    environment_updated: EnvironmentPublic
