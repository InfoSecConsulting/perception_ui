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


def upgrade():
  op.create_table('svc_nse_scripts',
                  sa.Column('id', sa.Integer, sa.Sequence('svc_nse_scripts_id_seq'), primary_key=True, nullable=False),
                  sa.Column('svc_id', sa.Integer, sa.ForeignKey('inventory_svcs.id', ondelete='cascade')),
                  sa.Column('name', sa.Text, nullable=False),
                  sa.Column('output', sa.Text, nullable=False))


def downgrade():
    pass
