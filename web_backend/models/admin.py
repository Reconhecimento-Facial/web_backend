from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from .base import table_registry


@table_registry.mapped_as_dataclass
class Admin:
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    date_of_birth: Mapped[date] = mapped_column()
    cpf: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column(unique=True)
    super_admin: Mapped[bool] = mapped_column()
