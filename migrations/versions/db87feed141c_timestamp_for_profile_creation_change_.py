"""timestamp for profile creation change var

Revision ID: db87feed141c
Revises: d32960d83384
Create Date: 2023-05-19 16:31:25.982306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db87feed141c'
down_revision = 'd32960d83384'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timeCreated', sa.DateTime(), nullable=True))
        batch_op.drop_column('profile_created')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_created', sa.DATETIME(), nullable=True))
        batch_op.drop_column('timeCreated')

    # ### end Alembic commands ###