from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import table_registry
from .user_environment import association_table


@table_registry.mapped_as_dataclass
class Environment:
    __tablename__ = 'environments'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    creator_admin_id: Mapped[int] = mapped_column(ForeignKey('admins.id'))
    users: Mapped[Optional[List['User']]] = relationship(  # noqa: F821  # type: ignore
        secondary=association_table, back_populates='environments', init=False
    )
