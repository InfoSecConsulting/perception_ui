"""create snmp_strings table

Revision ID: 22b0f462e1e
Revises: 17edc14f5f2
Create Date: 2015-10-25 14:22:18.961113

"""

# revision identifiers, used by Alembic.
revision = '22b0f462e1e'
down_revision = '17edc14f5f2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime

def _get_date():
    return datetime.datetime.now()

def upgrade():
  op.create_table('snmp_strings',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('community_string_encrypted', sa.String),
                  sa.Column('community_string_encrypted_salt', sa.String),
                  sa.Column('snmp_user_encrypted', sa.String),
                  sa.Column('snmp_user_encrypted_salt', sa.String),
                  sa.Column('snmp_group_encrypted', sa.String),
                  sa.Column('snmp_group_encrypted_salt', sa.String),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))

def downgrade():
    op.drop_table('snmp_strings')
