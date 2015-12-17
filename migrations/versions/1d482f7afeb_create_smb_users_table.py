"""create smb_users table

Revision ID: 1d482f7afeb
Revises: 42220a53132
Create Date: 2015-06-23 16:32:54.592331

"""

# revision identifiers, used by Alembic.
revision = '1d482f7afeb'
down_revision = '42220a53132'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

import datetime

def _get_date():
  return datetime.datetime.now()


def upgrade():
  op.create_table('smb_users',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('username', sa.String, nullable=False, unique=True),
                  sa.Column('encrypted_password', sa.String, nullable=False),
                  sa.Column('encrypted_password_salt', sa.String, nullable=False),
                  sa.Column('domain_name', sa.String, nullable=False),
                  sa.Column('description', sa.String),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))


def downgrade():
  op.drop_table('smb_users')
