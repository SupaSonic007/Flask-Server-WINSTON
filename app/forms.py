from flask_wtf import FlaskForm
from flask_login import current_user
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
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 16)])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(5, 128)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(8, 32)])
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
    subject = StringField("Subject", validators=[
                          DataRequired(), Length(1, 128)])
    body = TextAreaField("Body", validators=[DataRequired(), Length(1, 2000)])
    submit = SubmitField("Submit")


class AdminSQLForm(FlaskForm):
    query = TextAreaField("Query", validators=[DataRequired()])
    submit = SubmitField("Submit")


class EmptyForm(FlaskForm):
    submit = SubmitField("Submit")

class SaveForm(FlaskForm):
    save = SubmitField("Save")

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 16)])
    bio = TextAreaField('Bio', validators=[Length(0, 512)])
    submit = SubmitField("Submit")

    def validate_username(self, username) -> None:
        user = User.query.filter_by(username=username.data.lower()).first()
        if user and current_user.username != username.data.lower():
            raise ValidationError("Username taken")