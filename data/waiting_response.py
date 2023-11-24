import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class WaitingResponse(SqlAlchemyBase):
    __tablename__ = 'waiting_response'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    link_to_achievements = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    children_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('children.id'))
    children = orm.relationship('Children')
