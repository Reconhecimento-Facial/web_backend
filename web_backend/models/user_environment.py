from sqlalchemy import Column, ForeignKey, Table

from .base import table_registry

association_table = Table(
    'users_environments',
    table_registry.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('enviroment_id', ForeignKey('environments.id'), primary_key=True),
)
