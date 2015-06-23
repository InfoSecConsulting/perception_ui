"""create mac_vendors table

Revision ID: 42220a53132
Revises: 49a27be2c86
Create Date: 2015-06-23 16:30:39.218344

"""

# revision identifiers, used by Alembic.
revision = '42220a53132'
down_revision = '49a27be2c86'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.create_table('mac_vendors',
                  sa.Column('id', sa.Integer, sa.Sequence('mac_vendors_id_seq'), primary_key=True, nullable=False),
                  sa.Column('name', sa.Text, unique=True))


def downgrade():
    op.drop_table('mac_vendors')
