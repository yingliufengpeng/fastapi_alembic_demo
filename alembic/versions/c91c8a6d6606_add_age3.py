"""add age3

Revision ID: c91c8a6d6606
Revises: 9a7ebc08356d
Create Date: 2025-08-29 06:42:36.443212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c91c8a6d6606'
down_revision: Union[str, Sequence[str], None] = '9a7ebc08356d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
