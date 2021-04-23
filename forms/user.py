from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    nickname = StringField('Логин пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    nickname = StringField('Логин пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class SearchForm(FlaskForm):
    nickname = StringField('Ник игрока', validators=[DataRequired()])
    limit = IntegerField('Максимальное число партий', validators=[DataRequired()], default=1000000000)
    submit = SubmitField('Скачать')

