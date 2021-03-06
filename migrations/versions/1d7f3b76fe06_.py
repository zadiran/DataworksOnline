"""empty message

Revision ID: 1d7f3b76fe06
Revises: 0f1c5aa1cabc
Create Date: 2017-10-02 00:09:17.449393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d7f3b76fe06'
down_revision = '0f1c5aa1cabc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('datasets', sa.Column('guid', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'datasets', ['guid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'datasets', type_='unique')
    op.drop_column('datasets', 'guid')
    # ### end Alembic commands ###
