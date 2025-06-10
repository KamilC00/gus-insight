import time
from flask import Flask, jsonify, render_template, flash, request, redirect, Response, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm
from sample_visualisation import get_data
from passlib.hash import pbkdf2_sha256
import sqlite3
from init_db import init_db

init_db.init_db()

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

app.secret_key = '982dc81de5f6d6728bb379e537214175fbc805db0ba607c0f18a7d119103e277'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = str(id)
        self.username = username
        self.password = password
        self.authenticated = False
    
    def is_active(self):
        return self.is_active()
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return self.authenticated
    def is_active(self):
        return True
    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    curs.execute("SELECT * from users where id = (?)",[user_id])
    lu = curs.fetchone()
    if lu is None:
        return None
    else:
        return User(int(lu[0]), lu[1], lu[2])

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
     return redirect(url_for('chart'))
  form = LoginForm()
  if form.validate_on_submit():
     conn = sqlite3.connect('database.db')
     curs = conn.cursor()
     curs.execute("SELECT * FROM users where username = (?)",    [form.username.data])
     user = list(curs.fetchone())
     us = load_user(user[0])
     if form.username.data == us.username and pbkdf2_sha256.verify(form.password.data, us.password):
        login_user(us, remember=form.remember.data)
        uuser = list({form.username.data})[0].split('@')[0]
        flash('Logged in successfully '+uuser)
        return redirect(url_for('chart'))
     else:
        flash('Login Unsuccessfull.')
  return render_template('login.html',title='Login', form=form)

@app.route("/chart")
@login_required
def chart():
    chart = get_data()
    return render_template("index.html", chart=chart)

if __name__ == "__main__":
    app.run(debug=True)
