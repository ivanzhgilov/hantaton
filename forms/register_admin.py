from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class RegisterAdminForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    patronymic = StringField("Отчество", validators=[DataRequired()])
    position = StringField("Должность", validators=[DataRequired()])
    submit = SubmitField('Войти')
