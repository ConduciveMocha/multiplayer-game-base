"""empty message

Revision ID: f212a26adb2b
Revises: 
Create Date: 2019-04-25 05:43:46.248344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f212a26adb2b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=256), nullable=True),
    sa.Column('color', sa.String(length=24), nullable=True),
    sa.Column('mods', sa.String(length=256), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('thread_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['thread_id'], ['thread.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_thread',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('thread_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['thread_id'], ['thread.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_thread')
    op.drop_table('message')
    # ### end Alembic commands ###