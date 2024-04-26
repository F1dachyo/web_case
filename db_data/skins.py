import sqlalchemy
from .db_session import SqlAlchemyBase


class Skin(SqlAlchemyBase):
    __tablename__ = 'skins'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rarity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    image_bytes = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)