from xrabbitsmeme.db import db


class Wallet(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.BigInteger(), primary_key=True)
    address = db.Column(db.String(), nullable=False, unique=True)
