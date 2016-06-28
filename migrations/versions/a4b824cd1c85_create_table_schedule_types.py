"""create table schedule_types

Revision ID: a4b824cd1c85
Revises: 40ee1ca3cdc2
Create Date: 2016-06-27 12:10:32.817492

"""

# revision identifiers, used by Alembic.
revision = 'a4b824cd1c85'
down_revision = '40ee1ca3cdc2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime


def _get_date():
    return datetime.datetime.now()


def upgrade():
  op.create_table('schedule_types',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('name', sa.Text, nullable=False, unique=True),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date))


def downgrade():
  op.drop_table('schedule_types')
