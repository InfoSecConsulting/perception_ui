"""create vendors table

Revision ID: 4bbb8b6d5f6
Revises: 
Create Date: 2015-06-23 15:42:53.247610

"""

# revision identifiers, used by Alembic.
revision = '4bbb8b6d5f6'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.create_table('vendors',
                  sa.Column('id', sa.Integer, sa.Sequence('vendors_id_seq'), primary_key=True, nullable=False),
                  sa.Column('name', sa.Text, unique=True, nullable=False))

def downgrade():
    op.drop_table('vendors')