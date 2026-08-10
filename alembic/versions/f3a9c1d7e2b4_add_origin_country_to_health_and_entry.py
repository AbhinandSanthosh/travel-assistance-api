"""add origin_country_id to health_rules and entry_restrictions

Revision ID: f3a9c1d7e2b4
Revises: 44c4aa8e5a5d
Create Date: 2026-08-07 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3a9c1d7e2b4'
down_revision: Union[str, Sequence[str], None] = '44c4aa8e5a5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    Adds a nullable origin_country_id FK to health_rules and
    entry_restrictions so a rule can be scoped to the traveller's point
    of departure/embarkation (e.g. an Indian national flying to Poland
    via Saudi Arabia), not just their nationality. NULL is a deliberate
    "applies regardless of origin" wildcard, used as the fallback match
    when no origin-specific row exists — this is additive and backward
    compatible with all existing rows and callers.
    """
    op.add_column(
        'health_rules',
        sa.Column('origin_country_id', sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        'fk_health_rules_origin_country_id_countries',
        'health_rules',
        'countries',
        ['origin_country_id'],
        ['id'],
    )
    op.create_index(
        op.f('ix_health_rules_origin_country_id'),
        'health_rules',
        ['origin_country_id'],
        unique=False,
    )

    op.add_column(
        'entry_restrictions',
        sa.Column('origin_country_id', sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        'fk_entry_restrictions_origin_country_id_countries',
        'entry_restrictions',
        'countries',
        ['origin_country_id'],
        ['id'],
    )
    op.create_index(
        op.f('ix_entry_restrictions_origin_country_id'),
        'entry_restrictions',
        ['origin_country_id'],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f('ix_entry_restrictions_origin_country_id'),
        table_name='entry_restrictions',
    )
    op.drop_constraint(
        'fk_entry_restrictions_origin_country_id_countries',
        'entry_restrictions',
        type_='foreignkey',
    )
    op.drop_column('entry_restrictions', 'origin_country_id')

    op.drop_index(
        op.f('ix_health_rules_origin_country_id'),
        table_name='health_rules',
    )
    op.drop_constraint(
        'fk_health_rules_origin_country_id_countries',
        'health_rules',
        type_='foreignkey',
    )
    op.drop_column('health_rules', 'origin_country_id')
