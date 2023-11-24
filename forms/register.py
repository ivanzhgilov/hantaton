from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    patronymic = StringField("Отчество", validators=[DataRequired()])
    birthday = DateField("Дата рождения", validators=[DataRequired()])
    city = StringField("Город", validators=[DataRequired()])
    link_to_achievements = StringField("Ссылка", validators=[DataRequired()])
    areas_giftedness = StringField("Области одарённости", validators=[DataRequired()])
    submit = SubmitField('Регистрация')
