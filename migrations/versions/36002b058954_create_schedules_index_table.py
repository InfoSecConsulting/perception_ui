"""create schedules_index table

Revision ID: 36002b058954
Revises: 7c34e9a89bc0
Create Date: 2016-06-30 13:51:37.592662

"""

# revision identifiers, used by Alembic.
revision = '36002b058954'
down_revision = '7c34e9a89bc0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime


def _get_date():
    return datetime.datetime.now()


def upgrade():
  op.create_table('schedules_index',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('schedule_id', sa.Integer, sa.ForeignKey('schedules.id', ondelete='cascade'), nullable=False),
                  sa.Column('target_id', sa.Integer, sa.ForeignKey('targets.id', ondelete='cascade')),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date),
                  sa.Column('updated_at', sa.TIMESTAMP(timezone=False), onupdate=_get_date))


def downgrade():
  op.drop_table('schedules_index')
