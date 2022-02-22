from xrabbitsmeme.models import db


class Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.BigInteger(), primary_key=True)
    wallet_id = db.Column(db.BigInteger(), db.ForeignKey('wallets.id'))
