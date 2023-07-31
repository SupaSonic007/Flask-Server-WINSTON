import re
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from app.models import User


class LoginForm (FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username (Automatically Lowercase)', validators=[
                           DataRequired(), Length(3, 16, "Username must be between 3 and 16 characters long")])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(5, 128, "Email must be at least 5 characters long")])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(8, 32, "Password must be between 8 and 32 characters long")])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username) -> None:
        if User.query.filter_by(username=username.data.lower()).first():
            raise ValidationError("Username taken")

        username_regex_check(username)

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

        if user and user.username != current_user.username:
            raise ValidationError("Username taken")

        username_regex_check(username)


class ControllerForm(FlaskForm):
    controllerInput = StringField('Controller', validators=[DataRequired()])
    submit = SubmitField("Submit")

def username_regex_check(username):
    regex = re.compile(r"^[\-a-z0-9_\.]+$")
    if not regex.match(username.data.lower()):
        raise ValidationError("Invalid username. Username may not contain spaces or special characters besides '-', '_' & '.'")