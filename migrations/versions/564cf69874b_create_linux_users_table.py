"""create linux_users table

Revision ID: 564cf69874b
Revises: 1d482f7afeb
Create Date: 2015-06-23 16:45:18.964546

"""

# revision identifiers, used by Alembic.
revision = '564cf69874b'
down_revision = '1d482f7afeb'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime

def _get_date():
    return datetime.datetime.now()


def upgrade():
  op.create_table('linux_users',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('username', sa.String, nullable=False, unique=True),
                  sa.Column('encrypted_password', sa.String, nullable=False),
                  sa.Column('encrypted_password_salt', sa.String, nullable=False),
                  sa.Column('encrypted_enable_password', sa.String),
                  sa.Column('encrypted_enable_password_salt', sa.String),
                  sa.Column('description', sa.String),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date)),


def downgrade():
  op.drop_table('linux_users')
