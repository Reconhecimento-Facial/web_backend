from datetime import date

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


class AdminProfile(AdminPublic):
    date_of_birth: date
    cpf: str
    name: str
    phone_number: str


class Admins(BaseModel):
    admins: list[AdminPublic]
