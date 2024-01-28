"""empty message

Revision ID: a2d8a66418e6
Revises: acd2cc68a712
Create Date: 2023-11-28 15:19:12.692567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2d8a66418e6'
down_revision = 'acd2cc68a712'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('class_year', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(length=128), nullable=True),
    sa.Column('linkedin_url', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('more', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_column('more')

    op.drop_table('users')
    # ### end Alembic commands ###
