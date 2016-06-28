"""create table schedules

Revision ID: 35850e09007e
Revises: a4b824cd1c85
Create Date: 2016-06-27 12:10:33.079660

"""

# revision identifiers, used by Alembic.
revision = '35850e09007e'
down_revision = 'a4b824cd1c85'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime


def _get_date():
    return datetime.datetime.now()


def upgrade():
  op.create_table('schedules',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('name', sa.Text, nullable=False),
                  sa.Column('schedule_type_id', sa.Integer, sa.ForeignKey('schedule_types.id')),
                  sa.Column('start_date', sa.TIMESTAMP(timezone=False)),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))


def downgrade():
  op.drop_table('schedules')
