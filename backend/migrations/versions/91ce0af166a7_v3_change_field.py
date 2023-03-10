"""v3 change field

Revision ID: 91ce0af166a7
Revises: 9ced8a26f057
Create Date: 2023-02-18 12:31:43.222545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91ce0af166a7'
down_revision = '9ced8a26f057'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'text', new_column_name='content')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'content', new_column_name='text')
    # ### end Alembic commands ###
