from pydantic import BaseModel, EmailStr


class AdminSchema(BaseModel):
    email: EmailStr
    password: str
    super_admin: bool


class AdminPublicSchema(AdminSchema):
    id: int

    class Config:
        orm_mode=True

