"""create table days_of_the_week

Revision ID: 40ee1ca3cdc2
Revises: 74ff08dbdb8a
Create Date: 2016-06-27 12:10:32.562112

"""

# revision identifiers, used by Alembic.
revision = '40ee1ca3cdc2'
down_revision = '9d83e226662b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import datetime

def _get_date():
    return datetime.datetime.now()


def upgrade():
  op.create_table('days_of_the_week',
                  sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                  sa.Column('name', sa.Text, unique=True, nullable=False),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=False), default=_get_date))

def downgrade():
    op.drop_table('days_of_the_week')
