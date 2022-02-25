"""create material

Revision ID: 4d64a2d0abb2
Revises: af3f7dd28d9f
Create Date: 2022-02-25 19:27:38.124381

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4d64a2d0abb2'
down_revision = 'af3f7dd28d9f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('materials',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('category', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('filename', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('category_x_name', 'materials', ['category', 'name'], unique=True)
    op.drop_table('wallets')


def downgrade():
    op.create_table('wallets',
                    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
                    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='wallets_pkey'),
                    sa.UniqueConstraint('address', name='wallets_address_key')
                    )
    op.drop_index('category_x_name', table_name='materials')
    op.drop_table('materials')
