"""empty message

Revision ID: 025dd814df9c
Revises: 88028a4dd957
Create Date: 2019-08-16 12:04:40.799938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '025dd814df9c'
down_revision = '88028a4dd957'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'updated_at')
    # ### end Alembic commands ###