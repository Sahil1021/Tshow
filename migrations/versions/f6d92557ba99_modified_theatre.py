"""Modified theatre

Revision ID: f6d92557ba99
Revises: fa48b2be61ba
Create Date: 2023-07-22 15:25:38.726562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6d92557ba99'
down_revision = 'fa48b2be61ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('theatre', schema=None) as batch_op:
        batch_op.add_column(sa.Column('capacity', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('theatre', schema=None) as batch_op:
        batch_op.drop_column('capacity')

    # ### end Alembic commands ###
