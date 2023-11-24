import sqlalchemy
import datetime

from data.db_session import SqlAlchemyBase


class Child(SqlAlchemyBase):
    __tablename__ = 'children'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date_of_birth = sqlalchemy.Column(sqlalchemy.Date)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    link_to_achievements = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    areas_giftedness = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='нет')
    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
