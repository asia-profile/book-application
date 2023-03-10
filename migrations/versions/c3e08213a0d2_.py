"""empty message

Revision ID: c3e08213a0d2
Revises: 95c1944b48e6
Create Date: 2021-01-11 16:20:03.648584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3e08213a0d2'
down_revision = '95c1944b48e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('idea', schema=None) as batch_op:
        batch_op.drop_column('upvotes')
        batch_op.drop_column('downvotes')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('idea', schema=None) as batch_op:
        batch_op.add_column(sa.Column('downvotes', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('upvotes', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
