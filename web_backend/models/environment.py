from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import table_registry
from .user_environment import association_table


@table_registry.mapped_as_dataclass
class Environment:
    __tablename__ = 'environments'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(init=True, unique=True)
    name_unaccent: Mapped[str] = mapped_column(init=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    creator_admin_id: Mapped[int] = mapped_column(ForeignKey('admins.id'))
    users: Mapped[Optional[list['User']]] = relationship(  # noqa: F821  # type: ignore
        secondary=association_table, back_populates='environments', init=False
    )
    devices: Mapped[Optional[list['Device']]] = relationship(  # noqa: F821  # type: ignore
        back_populates='environment', init=False
    )
    __table_args__ = (
        Index(
            'idx_environments_name_gin_trgm',
            'name_unaccent',
            postgresql_using='gin',
            postgresql_ops={'name_unaccent': 'gin_trgm_ops'},
        ),
    )

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'name_unaccent': self.name_unaccent,
            'created_at': (
                self.created_at.isoformat() if self.created_at else None
            ),
            'updated_at': (
                self.updated_at.isoformat() if self.updated_at else None
            ),
            'creator_admin_id': self.creator_admin_id,
            'users': ([user.id for user in self.users] if self.users else []),
            'devices': (
                [device.id for device in self.devices] if self.devices else []
            ),
        }
