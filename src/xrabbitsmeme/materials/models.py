from ..db import db


class Material(db.Model):
    __tablename__ = 'materials'

    id = db.Column(db.BigInteger(), primary_key=True)
    category = db.Column(db.String(), nullable=False)
    name = db.Column(db.String())
    filename = db.Column(db.String())

    _category_x_name = db.Index('category_x_name', 'category', 'name', unique=True)
