"""add cities table and airports.city_id fk

Revision ID: e5f6a7b8c9d0
Revises: a1b2c3d4e5f6
Create Date: 2026-08-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5f6a7b8c9d0'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    NOTE: this migration documents a `cities` table and an
    `airports.city_id` column that were already created directly in
    Postgres via pgAdmin, ahead of the model/migration work. If those
    objects already exist in your target database, do NOT run
    `alembic upgrade head` on this revision -- it will fail with
    "relation already exists" / "column already exists". Instead run:

        alembic stamp head

    which marks this revision as applied without re-executing it. Only
    run the upgrade() below as-is against a database that does NOT yet
    have `cities` or `airports.city_id` (e.g. a fresh dev/test DB).
    """
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('city_code', sa.String(length=3), nullable=False),
        sa.Column('city_name', sa.String(length=100), nullable=False),
        sa.Column('country_id', sa.Integer(), nullable=False),
        sa.Column('timezone', sa.String(length=100), nullable=True),
        sa.Column(
            'active',
            sa.Boolean(),
            nullable=False,
            server_default='true',
        ),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ['country_id'],
            ['countries.id'],
            name='fk_cities_country_id',
        ),
        sa.UniqueConstraint('city_code', name='uq_cities_city_code'),
    )
    op.create_index(
        op.f('ix_cities_id'),
        'cities',
        ['id'],
        unique=False,
    )

    op.add_column(
        'airports',
        sa.Column('city_id', sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        'fk_airports_city_id',
        'airports',
        'cities',
        ['city_id'],
        ['id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'fk_airports_city_id',
        'airports',
        type_='foreignkey',
    )
    op.drop_column('airports', 'city_id')

    op.drop_index(
        op.f('ix_cities_id'),
        table_name='cities',
    )
    op.drop_table('cities')