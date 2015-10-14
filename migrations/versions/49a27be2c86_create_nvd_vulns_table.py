"""create nvd_vulns table

Revision ID: 49a27be2c86
Revises: 12022d803de
Create Date: 2015-06-23 15:56:52.716859

"""

# revision identifiers, used by Alembic.
revision = '49a27be2c86'
down_revision = '12022d803de'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('nvd_vulns',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('name', sa.Text, unique=True, nullable=False),
                    sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id'), nullable=False),
                    sa.Column('cveid', sa.Text, nullable=False),
                    sa.Column('vuln_published', sa.Text),
                    sa.Column('vuln_updated', sa.Text),
                    sa.Column('cvss', sa.Text),
                    sa.Column('cweid', sa.Text),
                    sa.Column('nvd_vuln_reference_id', sa.Integer, sa.ForeignKey('nvd_vuln_references.id')),
                    sa.Column('summary', sa.Text),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=False)),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=False)))


def downgrade():
    op.drop_table('nvd_vulns')
