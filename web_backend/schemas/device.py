from pydantic import BaseModel
from uuid import UUID

class DeviceSchema(BaseModel):
    id: UUID
    serial_number: str
    environment_id: int
    creator_admin_id: int
