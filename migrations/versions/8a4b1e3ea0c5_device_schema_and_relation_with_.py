"""device schema and relation with environment

Revision ID: 8a4b1e3ea0c5
Revises: 0b399c6f7e00
Create Date: 2025-01-12 08:24:13.434344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a4b1e3ea0c5'
down_revision: Union[str, None] = '0b399c6f7e00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'devices',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('serial_number', sa.String(), nullable=False),
        sa.Column('environment_id', sa.Integer(), nullable=True),
        sa.Column('creator_admin_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['creator_admin_id'], ['admins.id'], ),
        sa.ForeignKeyConstraint(['environment_id'], ['environments.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('environment_id'),
        sa.UniqueConstraint('serial_number')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('devices')
    # ### end Alembic commands ###
