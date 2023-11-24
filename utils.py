from data import db_session
from data.children import Child


def search_fullname(name, surname, patronymic):
    db_sess = db_session.create_session()
    child = db_sess.query(Child).filter(
        (Child.name == name) & (Child.surname == surname) & (Child.patronymic == patronymic)).first()
    if child:
        return child
    else:
        return "Not found"


# не работает если у детей несколько областей одарённости
def search_filters(filters: dict):
    db_sess = db_session.create_session()
    children = db_sess.query(Child).filter_by(**filters).all()
    if children:
        return children
    else:
        return "Not Found"
