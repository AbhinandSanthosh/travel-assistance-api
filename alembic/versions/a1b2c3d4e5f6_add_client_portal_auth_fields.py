"""add client portal auth fields (password hash, hashed api key)

Revision ID: a1b2c3d4e5f6
Revises: f3a9c1d7e2b4
Create Date: 2026-08-11 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'f3a9c1d7e2b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    Adds the columns needed for the client self-service portal:
      - contact_password_hash: bcrypt hash for portal login (mirrors
        users.password_hash).
      - api_key_hash / api_key_prefix / api_key_last_four /
        api_key_created_at / api_key_revoked_at: the hashed-key
        pattern replacing plaintext api_key lookups for new clients.

    The legacy `api_key` column is relaxed to nullable, since portal
    signups never populate it -- it's kept only so already-seeded
    clients created before the portal existed keep authenticating via
    the old plaintext-comparison path.
    """
    op.alter_column(
        'api_clients',
        'api_key',
        existing_type=sa.Text(),
        nullable=True,
    )

    op.add_column(
        'api_clients',
        sa.Column('contact_password_hash', sa.Text(), nullable=True),
    )
    op.add_column(
        'api_clients',
        sa.Column('api_key_hash', sa.Text(), nullable=True),
    )
    op.add_column(
        'api_clients',
        sa.Column('api_key_prefix', sa.String(), nullable=True),
    )
    op.add_column(
        'api_clients',
        sa.Column('api_key_last_four', sa.String(), nullable=True),
    )
    op.add_column(
        'api_clients',
        sa.Column('api_key_created_at', sa.DateTime(), nullable=True),
    )
    op.add_column(
        'api_clients',
        sa.Column('api_key_revoked_at', sa.DateTime(), nullable=True),
    )

    op.create_unique_constraint(
        'uq_api_clients_api_key_hash',
        'api_clients',
        ['api_key_hash'],
    )
    op.create_unique_constraint(
        'uq_api_clients_contact_email',
        'api_clients',
        ['contact_email'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'uq_api_clients_contact_email',
        'api_clients',
        type_='unique',
    )
    op.drop_constraint(
        'uq_api_clients_api_key_hash',
        'api_clients',
        type_='unique',
    )

    op.drop_column('api_clients', 'api_key_revoked_at')
    op.drop_column('api_clients', 'api_key_created_at')
    op.drop_column('api_clients', 'api_key_last_four')
    op.drop_column('api_clients', 'api_key_prefix')
    op.drop_column('api_clients', 'api_key_hash')
    op.drop_column('api_clients', 'contact_password_hash')

    op.alter_column(
        'api_clients',
        'api_key',
        existing_type=sa.Text(),
        nullable=False,
    )