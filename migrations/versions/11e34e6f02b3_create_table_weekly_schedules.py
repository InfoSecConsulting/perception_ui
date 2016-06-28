"""create table weekly_schedules

Revision ID: 11e34e6f02b3
Revises: 3da041cff701
Create Date: 2016-06-27 12:10:33.600612

"""

# revision identifiers, used by Alembic.
revision = '11e34e6f02b3'
down_revision = '3da041cff701'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime


def _get_date():
    return datetime.datetime.now()


def upgrade():
  op.create_table('weekly_schedules',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('schedule_id', sa.Integer, sa.ForeignKey('schedules.id'), nullable=False),
                  sa.Column('day_of_week_id', sa.Integer, sa.ForeignKey('days_of_the_week.id'), nullable=False),
                  sa.Column('time_of_day', sa.TIME, nullable=False),
                  sa.Column('start_date', sa.TIMESTAMP(timezone=False), nullable=False),
                  sa.Column('end_date', sa.TIMESTAMP(timezone=False)),
                  sa.Column('recurrence', sa.Integer, nullable=False),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))


def downgrade():
  op.drop_table('weekly_schedules')
