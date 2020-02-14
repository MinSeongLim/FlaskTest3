"""empty message

Revision ID: 651802f54b08
Revises: 900e01f48541
Create Date: 2020-02-04 16:55:50.489669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '651802f54b08'
down_revision = '900e01f48541'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('model',
    sa.Column('no', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('file', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('no'),
    mysql_collate='utf8_general_ci'
    )
    op.create_table('result',
    sa.Column('no', sa.Integer(), nullable=False),
    sa.Column('result', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('no'),
    mysql_collate='utf8_general_ci'
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('pw', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8_general_ci'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('result')
    op.drop_table('model')
    # ### end Alembic commands ###