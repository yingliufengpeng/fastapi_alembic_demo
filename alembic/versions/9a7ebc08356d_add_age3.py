"""add age3

Revision ID: 9a7ebc08356d
Revises: 5abcaa72ba77
Create Date: 2025-08-29 06:37:47.186064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a7ebc08356d'
down_revision: Union[str, Sequence[str], None] = '5abcaa72ba77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
