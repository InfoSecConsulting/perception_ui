"""create svc_nse_scripts table

Revision ID: 416322712fe
Revises: 392c3a6e915
Create Date: 2015-06-23 17:16:21.604533

"""

# revision identifiers, used by Alembic.
revision = '416322712fe'
down_revision = '392c3a6e915'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime


def _get_date():
    return datetime.datetime.now()

def upgrade():
  op.create_table('svc_nse_scripts',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('inventory_svc_id', sa.Integer, sa.ForeignKey('inventory_svcs.id', ondelete='cascade')),
                  sa.Column('name', sa.Text, nullable=False),
                  sa.Column('output', sa.Text, nullable=False),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))


def downgrade():
  op.drop_table('svc_nse_scripts')
