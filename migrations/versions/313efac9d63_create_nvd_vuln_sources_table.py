"""create nvd_vuln_sources table

Revision ID: 313efac9d63
Revises: 4fc9479a07
Create Date: 2015-06-23 15:53:45.782121

"""

# revision identifiers, used by Alembic.
revision = '313efac9d63'
down_revision = '4fc9479a07'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('nvd_vuln_sources',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('name', sa.Text))


def downgrade():
    op.create_drop('nvd_vuln_sources')

