"""copy models exact from tutorial

Revision ID: 3a4ba9bd3a53
Revises: 7ad94b1b409d
Create Date: 2024-08-20 23:47:35.508250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a4ba9bd3a53'
down_revision = '7ad94b1b409d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('body',
               existing_type=sa.VARCHAR(length=144),
               type_=sa.String(length=140),
               existing_nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=256), nullable=True))
        batch_op.drop_column('pw_hash')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pw_hash', sa.VARCHAR(length=256), nullable=True))
        batch_op.drop_column('password_hash')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('body',
               existing_type=sa.String(length=140),
               type_=sa.VARCHAR(length=144),
               existing_nullable=False)

    # ### end Alembic commands ###
