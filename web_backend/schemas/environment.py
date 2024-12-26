from datetime import datetime

from pydantic import BaseModel

from .message import Message
from .schemas_utils import form_body_environment_schema


@form_body_environment_schema
class EnvironmentSchema(BaseModel):
    name: str


class EnvironmentPublic(EnvironmentSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    creator_admin_id: int


class EnvironmentCreated(EnvironmentPublic):
    photo: str


class EnvironmentUpdated(Message):
    environment_updated: EnvironmentPublic

    class Config:
        from_attributes = True


class EnvironmentAux(BaseModel):
    id: int
    name: str


class EnvironmentAdded(Message):
    environment_added: EnvironmentAux
