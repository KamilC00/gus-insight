import time
from flask import Flask, jsonify, render_template, flash, request, redirect, Response, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm
from sample_visualisation import plot_unemployment_data, plot_inflation_data, plot_alcohol_data, plot_fuel_data, save_plot_to_db, get_plot_from_db, plot_cementary_data, plot_average_salary_data
from passlib.hash import pbkdf2_sha256
import sqlite3
import init_db 

init_db.init_db()

unemployment_plot = plot_unemployment_data()
if unemployment_plot:
  save_plot_to_db(unemployment_plot, "unemployment_by_gender")

inflation_plot = plot_inflation_data()
if inflation_plot:
  save_plot_to_db(inflation_plot, "inflation_trends")

alcohol_plot = plot_alcohol_data()
if alcohol_plot:
  save_plot_to_db(alcohol_plot, "alcohol_prices")

fuel_plot = plot_fuel_data()
if fuel_plot:
  save_plot_to_db(fuel_plot, "fuel_prices")
cementary_plot = plot_cementary_data()
if cementary_plot:
  save_plot_to_db(cementary_plot, "cementary_sizes")
salary_plot = plot_average_salary_data()
if salary_plot:
  save_plot_to_db(salary_plot, "salary_trends")

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
        curs.execute("SELECT * FROM users where username = (?)", [form.username.data])
        user_data = curs.fetchone()
        
        if user_data is None:
            flash('Login Unsuccessful.')
            return render_template('login.html', title='Login', form=form)
        
        user = list(user_data)
        us = load_user(user[0])
        
        if form.username.data == us.username and pbkdf2_sha256.verify(form.password.data, us.password):
            login_user(us, remember=form.remember.data)
            uuser = list({form.username.data})[0].split('@')[0]
            flash('Logged in successfully '+uuser)
            return redirect(url_for('chart'))
        else:
            flash('Login Unsuccessful.')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/chart")
@login_required
def chart():
    chart = get_plot_from_db("unemployment_by_gender")
    chart2 = get_plot_from_db("inflation_trends")
    chart3 = get_plot_from_db("alcohol_prices")
    chart4 = get_plot_from_db("fuel_prices")
    chart5 = get_plot_from_db("cementary_sizes")
    chart6 = get_plot_from_db("salary_trends")

    return render_template("index.html", chart=chart, chart2=chart2, chart3=chart3, chart4=chart4, chart5=chart5, chart6=chart6)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
