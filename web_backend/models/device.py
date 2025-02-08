from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import table_registry


@table_registry.mapped_as_dataclass
class Device:
    __tablename__ = 'devices'

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid4
    )
    serial_number: Mapped[str] = mapped_column(
        unique=True, nullable=False, init=True
    )
    environment_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('environments.id')
    )
    environment: Mapped['Environment'] = relationship(  # noqa: F821  # type: ignore
        back_populates='devices', single_parent=True
    )
    creator_admin_id: Mapped[int] = mapped_column(ForeignKey('admins.id'))

    def as_dict(self) -> dict:
        return {
            'id': str(self.id),
            'serial_number': self.serial_number,
            'environment_id': self.environment_id,
            'creator_admin_id': self.creator_admin_id,
        }
