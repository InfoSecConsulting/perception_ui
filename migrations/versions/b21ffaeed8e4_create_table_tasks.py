"""create table tasks

Revision ID: b21ffaeed8e4
Revises: 002116720e0b
Create Date: 2016-06-27 12:10:34.922896

"""

# revision identifiers, used by Alembic.
revision = 'b21ffaeed8e4'
down_revision = '002116720e0b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime


def _get_date():
    return datetime.datetime.now()


def upgrade():
  op.create_table('tasks',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('schedule_id', sa.Integer, sa.ForeignKey('schedules.id'), nullable=False),
                  sa.Column('run_date', sa.TIMESTAMP(timezone=False), nullable=False),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))


def downgrade():
  op.drop_table('tasks')
