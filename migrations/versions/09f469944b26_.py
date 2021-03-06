"""empty message

Revision ID: 09f469944b26
Revises: 99ffe5944c1a
Create Date: 2019-08-23 00:37:48.077630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09f469944b26'
down_revision = '99ffe5944c1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('environment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('object_effect',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('health', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('thread',
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('thread_hash', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=16), nullable=True),
    sa.Column('password_hash', sa.String(length=100), nullable=True),
    sa.Column('password_salt', sa.String(length=10), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=75), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game_object',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('posx', sa.Integer(), nullable=True),
    sa.Column('posy', sa.Integer(), nullable=True),
    sa.Column('acquirable', sa.Boolean(), nullable=True),
    sa.Column('collidable', sa.Boolean(), nullable=True),
    sa.Column('environment_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['environment_id'], ['environment.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory_object',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('use_effect', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['use_effect'], ['object_effect.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
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
    op.create_table('user_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('health', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_thread',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('thread_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['thread_id'], ['thread.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('game_inventory',
    sa.Column('game_object_id', sa.Integer(), nullable=True),
    sa.Column('inventory_object_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_object_id'], ['game_object.id'], ),
    sa.ForeignKeyConstraint(['inventory_object_id'], ['inventory_object.id'], )
    )
    op.create_table('user_inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('inventory_object_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inventory_object_id'], ['inventory_object.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_inventory')
    op.drop_table('game_inventory')
    op.drop_table('user_thread')
    op.drop_table('user_status')
    op.drop_table('message')
    op.drop_table('inventory_object')
    op.drop_table('game_object')
    op.drop_table('email')
    op.drop_table('user')
    op.drop_table('thread')
    op.drop_table('object_effect')
    op.drop_table('environment')
    # ### end Alembic commands ###
