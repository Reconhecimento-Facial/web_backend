from datetime import datetime

from pydantic import BaseModel

from .message import Message


class EnviromentSchema(BaseModel):
    name: str


class EnviromentPublic(EnviromentSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    creator_admin_id: int


class Enviroments(BaseModel):
    enviroments: list[EnviromentPublic]


class EnviromentUpdated(Message):
    enviroment_updated: EnviromentPublic
