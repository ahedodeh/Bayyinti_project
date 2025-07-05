from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '326126fc3076'
down_revision: Union[str, Sequence[str], None] = '271344a65497'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.alter_column(
        'property_listings',
        'location_lat',
        existing_type=sa.String(length=50),
        type_=sa.Float(),
        existing_nullable=True,
        postgresql_using="location_lat::double precision"
    )

    op.alter_column(
        'property_listings',
        'location_lon',
        existing_type=sa.String(length=50),
        type_=sa.Float(),
        existing_nullable=True,
        postgresql_using="location_lon::double precision"
    )

def downgrade() -> None:
    op.alter_column(
        'property_listings',
        'location_lat',
        existing_type=sa.Float(),
        type_=sa.String(length=50),
        existing_nullable=True,
        postgresql_using="location_lat::text"
    )

    op.alter_column(
        'property_listings',
        'location_lon',
        existing_type=sa.Float(),
        type_=sa.String(length=50),
        existing_nullable=True,
        postgresql_using="location_lon::text"
    )
