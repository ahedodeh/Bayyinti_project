"""add is_available column to rooms

Revision ID: 7f8ee8da28bd
Revises: None
Create Date: 2025-07-04 05:49:23.892388

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7f8ee8da28bd'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column(
        'rooms',
        sa.Column(
            'is_available',
            sa.Boolean(),
            nullable=True,
            server_default=sa.text('true')
        )
    )

def downgrade() -> None:
    op.drop_column('rooms', 'is_available')
