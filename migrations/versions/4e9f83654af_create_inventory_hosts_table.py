"""create inventory_hosts table

Revision ID: 4e9f83654af
Revises: 564cf69874b
Create Date: 2015-06-23 16:49:21.424298

"""

# revision identifiers, used by Alembic.
revision = '4e9f83654af'
down_revision = '564cf69874b'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa
import datetime

def _get_date():
    return datetime.datetime.now()


def upgrade():
    op.create_table('inventory_hosts',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('ipv4_addr', postgresql.INET, unique=True, nullable=False),
                    sa.Column('ipv6_addr', postgresql.INET, unique=True),
                    sa.Column('macaddr', postgresql.MACADDR),
                    sa.Column('host_type', sa.Text),
                    sa.Column('mac_vendor_id', sa.Integer, sa.ForeignKey('mac_vendors.id')),
                    sa.Column('state', sa.Text),
                    sa.Column('host_name', sa.Text),
                    sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id')),
                    sa.Column('arch', sa.Text),
                    sa.Column('smb_user_id', sa.Integer, sa.ForeignKey('smb_users.id')),
                    sa.Column('linux_user_id', sa.Integer, sa.ForeignKey('linux_users.id')),
                    sa.Column('info', sa.Text),
                    sa.Column('comments', sa.Text),
                    sa.Column('nvd_vuln_id', sa.Integer, sa.ForeignKey('nvd_vulns.id')),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))


def downgrade():
    op.drop_table('inventory_hosts')
