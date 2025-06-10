from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
import sqlite3
class LoginForm(FlaskForm):
 username = StringField('Login',validators=[DataRequired()])
 password = PasswordField('Password',validators=[DataRequired()])
 remember = BooleanField('Remember Me')
 submit = SubmitField('Login')
 def validate_login(self, login):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    curs.execute("SELECT username FROM users where username = (?)",[login.data])
    valemail = curs.fetchone()
    if valemail is None:
      raise ValidationError('This username is not registered. Please register before login')