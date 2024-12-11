from datetime import datetime

from pydantic import BaseModel


class EnviromentSchema(BaseModel):
    name: str


class EnviromentPublic(EnviromentSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    creator_admin_id: int


class Enviroments(BaseModel):
    enviroments: list[EnviromentPublic]