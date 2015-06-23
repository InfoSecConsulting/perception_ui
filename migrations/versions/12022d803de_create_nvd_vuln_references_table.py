"""create nvd_vuln_references table

Revision ID: 12022d803de
Revises: 313efac9d63
Create Date: 2015-06-23 15:55:42.158526

"""

# revision identifiers, used by Alembic.
revision = '12022d803de'
down_revision = '313efac9d63'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('nvd_vuln_references',
                    sa.Column('id', sa.Integer, sa.Sequence('nvd_vuln_references_id_seq'), primary_key=True, nullable=False),
                    sa.Column('nvd_vuln_source_id', sa.Integer, sa.ForeignKey('nvd_vuln_sources.id'), nullable=False),
                    sa.Column('nvd_ref_type', sa.Text),
                    sa.Column('href', sa.Text))


def downgrade():
    op.drop_table('nvd_vuln_references')
