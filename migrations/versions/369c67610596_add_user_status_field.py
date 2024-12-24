"""Add user status field

Revision ID: 369c67610596
Revises: adab90ee48f9
Create Date: 2024-12-23 21:47:18.535394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '369c67610596'
down_revision: Union[str, None] = 'adab90ee48f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE userstatus AS ENUM ('Ativado', 'Desativado')")
    op.add_column(
        'users', 
        sa.Column(
            'status', 
            sa.Enum('Ativado', 'Desativado', name='userstatus'), nullable=False, server_default='Ativado'
        )
    )


def downgrade() -> None:
    op.drop_column('users', 'status')
    op.execute("DROP TYPE userstatus")
