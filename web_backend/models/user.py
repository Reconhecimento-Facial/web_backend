from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import table_registry
from .user_environment import association_table


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    registered_by_admin_id: Mapped[int] = mapped_column(
        ForeignKey('admins.id')
    )
    registered_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    name: Mapped[str] = mapped_column(init=True)
    email: Mapped[str] = mapped_column(unique=True)
    date_of_birth: Mapped[date] = mapped_column()
    cpf: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str] = mapped_column(unique=True)
    environments: Mapped[Optional[list['Environment']]] = relationship(  # noqa: F821 # type: ignore
        secondary=association_table, back_populates='users', init=False
    )
