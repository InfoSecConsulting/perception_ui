"""create table one_time_schedules

Revision ID: 002116720e0b
Revises: 1a0a4c538570
Create Date: 2016-06-27 12:10:34.105006

"""

# revision identifiers, used by Alembic.
revision = '002116720e0b'
down_revision = '1a0a4c538570'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime


def _get_date():
    return datetime.datetime.now()


def upgrade():
  op.create_table('one_time_schedules',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('schedule_id', sa.Integer, sa.ForeignKey('schedules.id'), nullable=False),
                  sa.Column('start_date', sa.TIMESTAMP(timezone=False), nullable=False),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))


def downgrade():
  op.drop_table('one_time_schedules')
