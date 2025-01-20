"""Removing foreign key constraint from  last_accessed_environment_name on users table

Revision ID: 445a72fd0f81
Revises: 2043e80846bc
Create Date: 2025-01-20 05:42:24.629560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '445a72fd0f81'
down_revision: Union[str, None] = '2043e80846bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_last_accessed_environment_name_fkey', 'users', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('users_last_accessed_environment_name_fkey', 'users', 'environments', ['last_accessed_environment_name'], ['name'])
    # ### end Alembic commands ###
