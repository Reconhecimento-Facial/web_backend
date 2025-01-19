from .base import table_registry
from sqlalchemy import ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from datetime import datetime, date

@table_registry.mapped_as_dataclass
class AccessLog:
    __tablename__ = 'access_log'

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid4
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    user_name: Mapped[str] = mapped_column(init=True)
    user_name_unaccent: Mapped[str] = mapped_column(init=True)
    user_email: Mapped[str] = mapped_column(init=True)
    user_cpf: Mapped[str] = mapped_column(init=True)
    user_phone_number: Mapped[str] = mapped_column(init=True)

    environment_id: Mapped[int] = mapped_column(ForeignKey('environments.id'), nullable=True)
    environment_name: Mapped[str] = mapped_column(init=True)
    environment_name_unaccent: Mapped[str] = mapped_column(init=True)

    access_time: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    __table_args__ = (
        Index(
            'idx_access_log_users_name_gin_trgm',
            'user_name_unaccent',
            postgresql_using='gin',
            postgresql_ops={'user_name_unaccent': 'gin_trgm_ops'},
        ),
        Index(
            'idx_access_log_environment_name_gin_trgm',
            'environment_name_unaccent',
            postgresql_using='gin',
            postgresql_ops={'environment_name_unaccent': 'gin_trgm_ops'},
        ),
    )