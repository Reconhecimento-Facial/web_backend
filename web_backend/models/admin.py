from .base import table_registry

from sqlalchemy.orm import Mapped, mapped_column

@table_registry.mapped_as_dataclass
class Admin:
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    super_admin: Mapped[bool] = mapped_column(default=False)
