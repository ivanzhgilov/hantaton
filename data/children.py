import sqlalchemy
import datetime

from data.db_session import SqlAlchemyBase


class Child(SqlAlchemyBase):
    __tablename__ = 'children'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date_of_birth = sqlalchemy.Column(sqlalchemy.DateTime)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    telephone_number = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
 
