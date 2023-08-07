"""add DJ model

Revision ID: 84529e36d0de
Revises: 
Create Date: 2023-08-07 16:12:19.002981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84529e36d0de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('DJ',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('logged_in', sa.Boolean(), nullable=True),
    sa.Column('user_prefs', sa.PickleType(), nullable=True),
    sa.Column('saved_playlists', sa.ARRAY(sa.PickleType()), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('DJ')
    # ### end Alembic commands ###
