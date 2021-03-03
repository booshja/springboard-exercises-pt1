from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Username', validators=[InputRequired(
        'Username cannot be left blank')])
    password = PasswordField('Password', validators=[
        InputRequired('Password cannot be left blank')])
    email = StringField('Email Address', validators=[
        InputRequired('Email cannot be left blank')])
    first_name = StringField('First Name', validators=[
        InputRequired('First name cannot be left blank')])
    last_name = StringField('Last Name', validators=[
        InputRequired('Last name cannot be left blank')])


class LoginForm(FlaskForm):
    """Form for user login"""
    username = StringField('Username', validators=[InputRequired(
        'Username cannot be left blank')])
    password = PasswordField('Password', validators=[
        InputRequired('Password cannot be left blank')])


class FeedbackForm(FlaskForm):
    """Form for user feedback"""
    title = StringField('Title', validators=[
                        InputRequired('Title cannot be left blank')])
    content = StringField('Feedback', validators=[
                          InputRequired('Feedback cannot be left blank')])
