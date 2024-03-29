"""empty message

Revision ID: b2e7b77e7ee1
Revises: 
Create Date: 2021-07-06 07:07:18.336319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2e7b77e7ee1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('player',
    sa.Column('playerId', sa.String(length=48), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('groupId', sa.String(length=80), nullable=True),
    sa.Column('location', sa.String(length=80), nullable=True),
    sa.Column('orientation', sa.String(length=80), nullable=True),
    sa.Column('latitude', sa.Numeric(precision=6), nullable=True),
    sa.Column('longitude', sa.Numeric(precision=6), nullable=True),
    sa.Column('openingHours', sa.JSON(), nullable=True),
    sa.Column('specialHours', sa.JSON(), nullable=True),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('playerId')
    )
    op.create_table('player_state',
    sa.Column('playerId', sa.Integer(), nullable=False),
    sa.Column('playerState', sa.String(length=80), nullable=True),
    sa.Column('lastActive', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('playerId')
    )
    op.create_table('playout_plan',
    sa.Column('playoutId', sa.String(length=48), nullable=False),
    sa.Column('fromDate', sa.Date(), nullable=True),
    sa.Column('toDate', sa.Date(), nullable=True),
    sa.Column('fromTime', sa.Time(), nullable=True),
    sa.Column('toTime', sa.Time(), nullable=True),
    sa.Column('assetId', sa.String(length=48), nullable=True),
    sa.Column('playerIds', sa.JSON(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('assetLag', sa.Integer(), nullable=True),
    sa.Column('targeting', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('playoutId')
    )
    op.create_table('report_item',
    sa.Column('itemId', sa.Integer(), nullable=False),
    sa.Column('assetId', sa.String(length=48), nullable=True),
    sa.Column('playerId', sa.String(length=48), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('hour', sa.Integer(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('itemId')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('pub_date', sa.DateTime(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('report_item')
    op.drop_table('playout_plan')
    op.drop_table('player_state')
    op.drop_table('player')
    op.drop_table('category')
    # ### end Alembic commands ###
