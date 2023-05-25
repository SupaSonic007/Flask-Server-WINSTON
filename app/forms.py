from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from app import db
from app.models import User

class LoginForm (FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username) -> None:
        if User.query.filter_by(username=username.data.lower()).first():
            raise ValidationError("Username taken")
    
    def validate_email(self, email) -> None:
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email taken")

class PostForm(FlaskForm):
    subject = StringField("Subject", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AdminSQLForm(FlaskForm):
    query = TextAreaField("Query", validators=[DataRequired()])
    submit = SubmitField("Submit")
