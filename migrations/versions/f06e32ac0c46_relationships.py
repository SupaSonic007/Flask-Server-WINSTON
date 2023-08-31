"""relationships

Revision ID: f06e32ac0c46
Revises: 
Create Date: 2023-08-28 10:50:21.453208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f06e32ac0c46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=16), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('time_created', sa.DateTime(), nullable=True),
    sa.Column('password_hashed', sa.String(length=128), nullable=True),
    sa.Column('bio', sa.String(length=512), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('collection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_collection_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_collection'))
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('header', sa.String(length=128), nullable=True),
    sa.Column('body', sa.String(length=2000), nullable=True),
    sa.Column('imageLocation', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_post_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_post')),
    sa.UniqueConstraint('imageLocation', name=op.f('uq_post_imageLocation'))
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_timestamp'), ['timestamp'], unique=False)

    op.create_table('collection_for_posts',
    sa.Column('collection_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['collection_id'], ['collection.id'], name=op.f('fk_collection_for_posts_collection_id_collection'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name=op.f('fk_collection_for_posts_post_id_post'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('collection_id', 'post_id', name=op.f('pk_collection_for_posts'))
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=2000), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name=op.f('fk_comment_post_id_post'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_comment_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comment'))
    )
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_comment_timestamp'), ['timestamp'], unique=False)

    op.create_table('like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name=op.f('fk_like_post_id_post'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_like_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_like'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('like')
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_comment_timestamp'))

    op.drop_table('comment')
    op.drop_table('collection_for_posts')
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_timestamp'))

    op.drop_table('post')
    op.drop_table('collection')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###