from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from sqlalchemy import select

from data.user import User
from data.jobs import Jobs
from data import db_session
from forms.register import RegisterForm
from forms.emergency_access import EmergencyAccess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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
    title = "works"
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    team_leaders = []
    for job in jobs:
        leader = db_sess.query(User).filter(User.id == job.team_leader)[0]
        leader_name = f"{leader.surname} {leader.name}"
        team_leaders.append(leader_name)
    return render_template('journal_works.html', title=title, jobs=jobs, team_leaders=team_leaders)


@app.route('/training/<prof>')
def training(prof):
    title = "Тренировочный центр"
    if "инженер" in prof or "строитель" in prof:
        professional_orientation = "Инженерные тренажеры"
    else:
        professional_orientation = "Научные симуляторы"
    return render_template('training.html', title=title, professional_orientation=professional_orientation)


@app.route('/list_prof/<display_method>')
def list_prof(display_method):
    list_professions = ["инженер-исследователь", "пилот", "строитель", "экзобиолог", "врач",
                        "инженер по терраформированию", "климатолог", "спеиалист по радиаионной защите", "астролог",
                        "гляциолог", "инженер жизнеобеспечения", "метеоролог", "оператор марсохода", "киберинженер",
                        "штурман", "пилот дронов"]
    return render_template('list_prof.html', list_professions=list_professions, display_methodist=display_method)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    values = {
        'title': "Анкета",
        'surname': "Watny",
        'name': "Mark",
        'education': "выше среднего",
        'profession': "штурман марсохода",
        'sex': "male",
        'motivation': "Всегда мечтал застрять на Марсе!",
        'ready': True
    }
    return render_template('auto_answer.html', **values)


@app.route('/emergency_access', methods=['GET', 'POST'])
def login():
    form = EmergencyAccess()
    access = False
    if form.validate_on_submit():
        access = True
    return render_template('emergency_access.html', title='Авторизация', form=form, access=access)


@app.route('/distribution')
def distribution():
    astronauts = ["Ридли Скотт", "Энди Уир", "Марк Уотни", "Венката Капур", "Тедди Сандерс", "Шон Бин"]
    return render_template('distribution.html', astronauts=astronauts)


@app.route('/table/<sex>/<age>')
def table(sex, age):
    return render_template('table.html', age=int(age), sex=sex)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="одна почта - один человек")
        if db_sess.query(User).filter(User.surname == form.surname.data, User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="ну ладно одинаковые имена, ладно фамилии, но по отдельности")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
