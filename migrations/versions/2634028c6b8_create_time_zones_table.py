"""create time_zones table

Revision ID: 2634028c6b8
Revises: 22b0f462e1e
Create Date: 2015-10-25 14:22:32.045292

"""

# revision identifiers, used by Alembic.
revision = '2634028c6b8'
down_revision = '22b0f462e1e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime

def _get_date():
  return datetime.datetime.now()

def upgrade():
  op.create_table('time_zones',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('name', sa.String(128), nullable=False, unique=True),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))

def downgrade():
  op.drop_table('time_zones')
