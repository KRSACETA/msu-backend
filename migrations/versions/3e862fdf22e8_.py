"""empty message

Revision ID: 3e862fdf22e8
Revises: 757c902e2498
Create Date: 2020-04-02 18:24:33.467545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e862fdf22e8'
down_revision = '757c902e2498'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('desc', sa.Text(), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('inserted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link')
    # ### end Alembic commands ###
