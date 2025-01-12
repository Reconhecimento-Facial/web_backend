from pydantic import BaseModel


class DeviceSchema(BaseModel):
    serial_number: str
    environment_id: int
    creator_admin_id: int
