from ..db import db


class NFTSeries(db.Model):
    __tablename__ = 'nftseries'
    '''
    NFT 系列，如：X Rabbits Club
    ipfs_path 为在合约中 TokenURI，去掉 ipfs 的 path
    如：
    1. X Rabbits #6559 的 TokenURI 为 ipfs://QmShUrXkgxjQ1eeCuo7hywsK42cGYj6KQ8N5XomM7d9A9M/6559
       ipfs_path 为 QmShUrXkgxjQ1eeCuo7hywsK42cGYj6KQ8N5XomM7d9A9M
    2. 小幽灵 #1 的 TokenURI 为 https://ipfs.io/ipfs/QmU61BwmB9fm3kN4EWS14YxrB1FFJcMWj9GRrf4hsEvaYE/1
       ipfs_path 为 QmU61BwmB9fm3kN4EWS14YxrB1FFJcMWj9GRrf4hsEvaYE
    supply 为合约中的 totalSupply
    '''

    id = db.Column(db.BigInteger(), primary_key=True)
    ipfs_path = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    supply = db.Column(db.Integer(), nullable=False, default=0)


class NFT(db.Model):
    __tablename__ = 'nfts'
    '''
    对应 NFT 系列中的每一个 NFT
    info 为 ipfs info
    filename 为将原图存在本地的路径
    '''

    id = db.Column(db.BigInteger(), primary_key=True)
    series_id = db.Column(db.ForeignKey('nftseries.id'), nullable=False)
    no = db.Column(db.Integer(), nullable=False)
    info = db.Column(db.String(), nullable=True)
    filename = db.Column(db.String(), nullable=True)

    _series_id_x_no = db.Index('series_id_x_no', 'series_id', 'no', unique=True)


# todo 完善切图类别，手工切图/自动切图？跑脚本将切图存入服务器
class GraphCategory(db.Model):
    __tablename__ = 'graph_categories'
    '''
    NFT 切图的类别
    如：
    X Rabbits 可以切图为 1. 透明背景兔子 2. 兔子头
    '''

    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    nft_id = db.Column(db.ForeignKey('nfts.id'), nullable=False)


# todo 完善切图类别，手工切图/自动切图？跑脚本将切图存入服务器
class NFTGraph(db.Model):
    __tablename__ = 'nft_graphs'
    '''
    NFT 切图
    对应一个 NFT 系列，对应这个系列中的某一个类别
    '''

    id = db.Column(db.BigInteger(), primary_key=True)
    filename = db.Column(db.String(), nullable=False)
    nft_id = db.Column(db.ForeignKey('nfts.id'), nullable=False)
    graph_id = db.Column(db.ForeignKey('graph_categories.id'), nullable=False)
