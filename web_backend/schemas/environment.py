from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

from fastapi import Query
from pydantic import BaseModel

from .message import Message
from .schemas_utils import form_body_environment_schema
from .device import DeviceSchema

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
    devices: Optional[list[DeviceSchema]]


class EnvironmentUpdated(Message):
    class EnvironmentPublicUpdated(EnvironmentPublic):
        photo_url: str

    environment_updated: EnvironmentPublicUpdated
    devices: Optional[list[DeviceSchema]]

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
