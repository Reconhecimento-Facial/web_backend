from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import Query
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


class EnvironmentPublicWithPhotoURL(EnvironmentPublic):
    photo_url: str


class EnvironmentCreated(EnvironmentPublic):
    photo_url: str


class EnvironmentUpdated(Message):
    class EnvironmentPublicUpdated(EnvironmentPublic):
        photo_url: str

    environment_updated: EnvironmentPublicUpdated
    devices_serial_numbers: list[str] | None

    class Config:
        from_attributes = True


class EnvironmentAux(BaseModel):
    id: int
    name: str


class EnvironmentAdded(Message):
    environment_added: EnvironmentAux


class EnvironmentFilter(BaseModel):
    class AscendingOrDescending(str, Enum):
        ascending = 'ascending'
        descending = 'descending'

    name: Annotated[
        str | None, Query(None, description='Filter by environment name')
    ] = None
    sort_order: Annotated[
        AscendingOrDescending | None,
        Query(None, description='Sort in ascending or descending order'),
    ] = None
