"""empty message

Revision ID: 95c1944b48e6
Revises: 05018879706b
Create Date: 2021-01-11 14:56:01.225165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95c1944b48e6'
down_revision = '05018879706b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('idea',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=500), nullable=True),
    sa.Column('upvotes', sa.Integer(), nullable=True),
    sa.Column('downvotes', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('idea', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_idea_text'), ['text'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('idea', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_idea_text'))

    op.drop_table('idea')
    # ### end Alembic commands ###
