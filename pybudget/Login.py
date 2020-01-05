from flask import g

from pybudget import login, auth
from pybudget.DB import User, get_session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


@login.user_loader
def load_user(id):
    return get_session().query(User).get(int(id))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@auth.verify_password
def verify_password(username, password):
    user = get_session().query(User).filter_by(username=username).first()
    if not user or not user.check_password(password):
        return False
    g.user = user
    return True
