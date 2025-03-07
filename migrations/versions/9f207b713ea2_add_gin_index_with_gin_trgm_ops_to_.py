"""Add gin index with gin_trgm_ops to environments.name_unaccent column

Revision ID: 9f207b713ea2
Revises: 80ed89d55f94
Create Date: 2024-12-26 16:30:14.611925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f207b713ea2'
down_revision: Union[str, None] = '80ed89d55f94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'environments',
        sa.Column('name_unaccent', sa.String(), nullable=True)
    )
    op.execute(
        """
        UPDATE environments
        SET name_unaccent = unaccent(name)
        """
    )
    op.alter_column(
        'environments',
        'name_unaccent',
        nullable=False
    )
    op.create_index(
        'idx_environments_name_gin_trgm',
        'environments',
        ['name_unaccent'],
        unique=False,
        postgresql_using='gin',
        postgresql_ops={'name_unaccent': 'gin_trgm_ops'}
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        'idx_environments_name_gin_trgm',
        table_name='environments',
        postgresql_using='gin',
        postgresql_ops={'name_unaccent': 'gin_trgm_ops'}
    )
    op.drop_column('environments', 'name_unaccent')
    # ### end Alembic commands ###
