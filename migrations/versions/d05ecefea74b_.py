"""empty message

Revision ID: d05ecefea74b
Revises: e81f5f61b865
Create Date: 2017-10-14 00:31:47.923602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd05ecefea74b'
down_revision = 'e81f5f61b865'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('datasets', sa.Column('distinctive_name', sa.String(), nullable=True))
    op.add_column('datasets', sa.Column('separator', sa.String(), server_default=';', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('datasets', 'separator')
    op.drop_column('datasets', 'distinctive_name')
    # ### end Alembic commands ###
