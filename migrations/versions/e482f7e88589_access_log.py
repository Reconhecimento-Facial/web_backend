"""access_log

Revision ID: e482f7e88589
Revises: fc13b3725136
Create Date: 2025-01-19 00:06:51.142133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e482f7e88589'
down_revision: Union[str, None] = 'fc13b3725136'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'access_log',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('user_name', sa.String(), nullable=False),
        sa.Column('user_name_unaccent', sa.String(), nullable=False),
        sa.Column('user_email', sa.String(), nullable=False),
        sa.Column('user_cpf', sa.String(), nullable=False),
        sa.Column('user_phone_number', sa.String(), nullable=False),
        sa.Column('environment_id', sa.Integer(), nullable=True),
        sa.Column('environment_name', sa.String(), nullable=False),
        sa.Column('environment_name_unaccent', sa.String(), nullable=False),
        sa.Column('access_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('allowed_access', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['environment_id'], ['environments.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'idx_access_log_environment_name_gin_trgm',
        'access_log',
        ['environment_name_unaccent'],
        unique=False,
        postgresql_using='gin',
        postgresql_ops={'environment_name_unaccent': 'gin_trgm_ops'}
    )
    op.create_index(
        'idx_access_log_users_name_gin_trgm',
        'access_log',
        ['user_name_unaccent'],
        unique=False,
        postgresql_using='gin',
        postgresql_ops={'user_name_unaccent': 'gin_trgm_ops'}
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        'idx_access_log_users_name_gin_trgm',
        table_name='access_log',
        postgresql_using='gin',
        postgresql_ops={'user_name_unaccent': 'gin_trgm_ops'}
    )
    op.drop_index(
        'idx_access_log_environment_name_gin_trgm',
        table_name='access_log',
        postgresql_using='gin',
        postgresql_ops={'environment_name_unaccent': 'gin_trgm_ops'}
    )
    op.drop_table('access_log')
    # ### end Alembic commands ###
