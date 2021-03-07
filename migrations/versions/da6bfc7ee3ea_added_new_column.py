"""added new column.

Revision ID: da6bfc7ee3ea
Revises: 634b94331b18
Create Date: 2020-12-29 13:30:19.952409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da6bfc7ee3ea'
down_revision = '634b94331b18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('bio', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('job', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'job')
    op.drop_column('users', 'bio')
    # ### end Alembic commands ###
