from pydantic import BaseModel

class AdminSchema(BaseModel):
    username: str
    password: str
    super_admin: bool