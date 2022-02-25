"""create nfts

Revision ID: af3f7dd28d9f
Revises: 1da53d73a4ec
Create Date: 2022-02-25 16:17:29.975285

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'af3f7dd28d9f'
down_revision = '1da53d73a4ec'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('nftseries',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('ipfs_path', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('supply', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('ipfs_path')
                    )
    op.create_table('nfts',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('series_id', sa.BigInteger(), nullable=False),
                    sa.Column('no', sa.Integer(), nullable=False),
                    sa.Column('info', sa.String(), nullable=True),
                    sa.Column('filename', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['series_id'], ['nftseries.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('series_id_x_no', 'nfts', ['series_id', 'no'], unique=True)
    op.create_table('graph_categories',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('nft_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['nft_id'], ['nfts.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('nft_graphs',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('filename', sa.String(), nullable=False),
                    sa.Column('nft_id', sa.BigInteger(), nullable=False),
                    sa.Column('graph_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['graph_id'], ['graph_categories.id'], ),
                    sa.ForeignKeyConstraint(['nft_id'], ['nfts.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_table('resources')


def downgrade():
    op.create_table('resources',
                    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
                    sa.Column('wallet_id', sa.BIGINT(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['wallet_id'], ['wallets.id'], name='resources_wallet_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='resources_pkey')
                    )
    op.drop_table('nft_graphs')
    op.drop_table('graph_categories')
    op.drop_index('series_id_x_no', table_name='nfts')
    op.drop_table('nfts')
    op.drop_table('nftseries')
