"""create target table

Revision ID: 9d83e226662b
Revises: 4e051e1c257
Create Date: 2016-04-01 20:33:15.866165

"""

# revision identifiers, used by Alembic.
revision = '9d83e226662b'
down_revision = '4e051e1c257'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa
import datetime

def _get_date():
    return datetime.datetime.now()


def upgrade():
  op.create_table('targets',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('ip_addr', postgresql.INET, unique=True),
                  sa.Column('subnet', postgresql.CIDR, unique=True),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))

def downgrade():
    op.drop_table('targets')
