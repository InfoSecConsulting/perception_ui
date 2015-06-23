"""create local_nets table

Revision ID: 3b8f731f438
Revises: 416322712fe
Create Date: 2015-06-23 17:50:53.379997

"""

# revision identifiers, used by Alembic.
revision = '3b8f731f438'
down_revision = '416322712fe'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa
import datetime

def _get_date():
    return datetime.datetime.now()

def upgrade():
  op.create_table('local_nets',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('subnet', postgresql.CIDR, unique=True),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date)),


def downgrade():
  op.drop_table('local_nets')
