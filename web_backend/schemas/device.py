from uuid import UUID

from pydantic import BaseModel


class DeviceSchema(BaseModel):
    id: UUID
    serial_number: str
    environment_id: int
    creator_admin_id: int
