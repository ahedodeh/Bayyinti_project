"""add entity_type to images

Revision ID: 271344a65497
Revises: 7f8ee8da28bd
Create Date: 2025-07-05 12:13:37.769783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '271344a65497'
down_revision: Union[str, Sequence[str], None] = '7f8ee8da28bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.add_column('images', sa.Column('entity_type', sa.String(length=50), nullable=True))


def downgrade():
    op.drop_column('images', 'entity_type')