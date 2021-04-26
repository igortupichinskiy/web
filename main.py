import requests
from flask import Flask, render_template, redirect, send_file
from data import db_session
from forms.user import RegisterForm, LoginForm, SearchForm
from data.users import User
from flask_login import LoginManager, login_user, logout_user, login_required
from waitress import serve


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    serve(app, host='0.0.0.0', port=5000)


@app.route('/', methods=['GET', 'POST'])
def lichess_download():
    form = SearchForm()
    if form.validate_on_submit():
        lichess_request = "https://lichess.org/api/games/user/"
        nick = form.nickname.data
        final_request = lichess_request + nick + "?max=" + str(form.limit.data)
        response = requests.get(final_request)
        if response:
            with open('cash.pgn', mode="wb") as f:
                f.write(response.content)
            return send_file('cash.pgn', as_attachment=True, attachment_filename=f"{nick}.pgn")
    return render_template('main_page.html', title='Скачать партии', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(nickname=form.nickname.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


#  if __name__ == '__main__':
db_session.global_init('db/users.db')
