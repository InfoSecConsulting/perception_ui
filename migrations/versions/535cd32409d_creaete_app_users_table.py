"""creaete app users table

Revision ID: 535cd32409d
Revises: f5e18e930c
Create Date: 2015-10-21 16:09:57.103976

"""

# revision identifiers, used by Alembic.
revision = '535cd32409d'
down_revision = 'f5e18e930c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime

def _get_date():
  return datetime.datetime.now()

def upgrade():
  op.create_table('app_users',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('username', sa.String(128), nullable=False, unique=True),
                  sa.Column('firstname', sa.String(128)),
                  sa.Column('lastname', sa.String(128)),
                  sa.Column('email', sa.String(128), nullable=False),
                  sa.Column('phone', sa.VARCHAR(12)),
                  sa.Column('company', sa.String(32)),
                  sa.Column('password_hash', sa.String(255), nullable=False),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))


def downgrade():
  op.drop_table('app_users')
