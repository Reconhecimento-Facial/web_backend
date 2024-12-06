from pydantic import BaseModel, EmailStr


class AdminSchema(BaseModel):
    email: EmailStr
    password: str
    super_admin: bool


class AdminDB(AdminSchema):
    id: int


class AdminPublic(BaseModel):
    id: int
    email: EmailStr
    super_admin: bool

    class Config:
        from_attributes = True


class Admins(BaseModel):
    admins: list[AdminPublic]
