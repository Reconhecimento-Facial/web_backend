from datetime import datetime
from enum import Enum

from sqlalchemy import Column, ForeignKey, Table, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


workers_groups = Table(
    'workers_groups',
    table_registry.metadata,
    Column('worker_id', ForeignKey('workers.id'), primary_key=True),
    Column('group_id', ForeignKey('groups.id'), primary_key=True),
)

workers_envs = Table(
    'workers_envs',
    table_registry.metadata,
    Column('worker_id', ForeignKey('workers.id'), primary_key=True),
    Column('env_id', ForeignKey('envs.id'), primary_key=True),
)

groups_envs = Table(
    'groups_envs',
    table_registry.metadata,
    Column('group_id', ForeignKey('groups.id'), primary_key=True),
    Column('env_id', ForeignKey('envs.id'), primary_key=True),
)


class WorkerStatus(str, Enum):
    active = 'active'
    disabled = 'disabled'


@table_registry.mapped_as_dataclass
class Worker:
    __tablename__ = 'workers'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    status: Mapped[WorkerStatus] = mapped_column(
        init=False, default=WorkerStatus.disabled
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    
    groups: Mapped[list['Group']] = relationship(
        init=False, secondary=workers_groups, back_populates='workers'
    )
    envs: Mapped[list['Enviroment']] = relationship(
        init=False, secondary=workers_envs, back_populates='workers'
    )


@table_registry.mapped_as_dataclass
class Group:
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(init=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    workers: Mapped[list['Worker']] = relationship(
        init=False, secondary=workers_groups, back_populates='groups'
    )
    envs: Mapped[list['Enviroment']] = relationship(
        init=False, secondary=groups_envs, back_populates='groups'
    )


@table_registry.mapped_as_dataclass
class Enviroment:
    __tablename__ = 'envs'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(init=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    workers: Mapped[list['Worker']] = relationship(
        init=False, secondary=workers_envs, back_populates='envs'
    )
    groups: Mapped[list[Group]] = relationship(
        init=False, secondary=groups_envs, back_populates='envs'
    )
