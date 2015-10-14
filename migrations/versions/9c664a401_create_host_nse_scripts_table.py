"""create host_nse_scripts table

Revision ID: 9c664a401
Revises: 4e9f83654af
Create Date: 2015-06-23 17:06:57.311177

"""

# revision identifiers, used by Alembic.
revision = '9c664a401'
down_revision = '4e9f83654af'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.create_table('host_nse_scripts',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('host_id', sa.Integer, sa.ForeignKey('inventory_hosts.id', ondelete='cascade')),
                  sa.Column('name', sa.Text, nullable=False),
                  sa.Column('output', sa.Text, nullable=False))


def downgrade():
  op.drop_table('host_nse_scripts')
