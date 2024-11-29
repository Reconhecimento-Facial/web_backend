from pydantic import BaseModel, EmailStr


class AdminSchema(BaseModel):
    email: EmailStr
    password: str
    super_admin: bool


class AdminPublicSchema(AdminSchema):
    id: int

    class Config:
        from_attributes = True


class Admins(BaseModel):
    admins: list[AdminPublicSchema]
