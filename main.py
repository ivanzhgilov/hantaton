from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import login_user, LoginManager, logout_user, login_required, current_user

from data import db_session
from data.admins import Admin
from data.children import Child
from data.waiting_response import WaitingResponse
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.register_admin import RegisterAdminForm
from utils import search_fullname, search_filters

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init('db/blogs.sqlite')
    app.run(host='0.0.0.0', port=8000, debug=True)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.submit.data:
            db_sess = db_session.create_session()
            user = db_sess.query(Child, Admin).filter(
                Child.email == form.email.data | Admin.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    form = RegisterAdminForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return "пароли не совпадают"
        db_sess = db_session.create_session()
        if db_sess.query(Admin).filter(Admin.email == form.email.data).first():
            return "одна почта"
        if db_sess.query(User).filter(User.surname == form.surname.data, User.name == form.name.data).first():
            return "сотрудник зарегистрирован"
        admin = Admin(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            patronymic=form.patronymic.data,
            position=form.position.data,
        )
        admin.set_password(form.password.data)
        db_sess.add(admin)
        db_sess.commit()
        return redirect("/admin_main_window")
    return "файл html регистрации"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('reg.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Child).filter(Child.email == form.email.data).first():
            return render_template('reg.html', title='Регистрация',
                                   form=form,
                                   message="одна почта - один человек")
        if db_sess.query(Child).filter(Child.surname == form.surname.data, Child.name == form.name.data).first():
            return render_template('reg.html', title='Регистрация', form=form,
                                   message="ну ладно одинаковые имена, ладно фамилии, но по отдельности")
        child = Child(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            patronymic=form.patronymic.data,
            birthday=form.birthday.data,
            city=form.city.data,
            link_to_achievements=form.link_to_achievements.data,
            areas_giftedness=form.areas_giftedness.data
        )
        child.set_password(form.password.data)
        db_sess.add(child)
        db_sess.commit()
        return redirect('/login')
    return render_template('reg.html', title='Регистрация', form=form)


@app.route('/personal_account', methods=['GET', 'POST'])
def personal_account():
    pass


@app.route('/admin_main_window', methods=['GET', 'POST'])
def admin_main_window():
    pass


@app.route('/search', methods=['GET', 'POST'])
def search():
    pass


@app.route('/viewing_applications', methods=['GET', 'POST'])
def viewing_applications():
    pass


if __name__ == '__main__':
    main()
