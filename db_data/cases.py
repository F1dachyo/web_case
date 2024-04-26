import sqlalchemy
from .db_session import SqlAlchemyBase


class Case(SqlAlchemyBase):
    __tablename__ = 'cases'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    image_bytes = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    skins_ids = sqlalchemy.Column(sqlalchemy.String, nullable=True)