import re
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from app.models import User

# Forms for the website have format:
# class <name>(FlaskForm):
#     <Form Attribute Name> = <Form Attribute Type>(<label>, validators=[<validators>])
#
#     def <Validate Attribute or Perform Checks>(self, <attribute>):
#         if <attribute> is invalid
#             raise ValidationError("<Error Message>")

class LoginForm (FlaskForm):
    '''
    Form for logging in

    Attributes:
        username (StringField): Username field
        password (PasswordField): Password field
        remember_me (BooleanField): Remember me field
        submit (SubmitField): Submit button
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    '''
    Form for registering a user

    Attributes:
        username (StringField): Username field
        email (StringField): Email field
        email2 (StringField): Email confirmation field
        password (PasswordField): Password field
        password2 (PasswordField): Password confirmation field
        submit (SubmitField): Submit button

    Methods:
        validate_username: Checks if username is taken
    '''
    username = StringField('Username (Automatically Lowercase)', validators=[
                           DataRequired(), Length(3, 16, "Username must be between 3 and 16 characters long")])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(5, 128, "Email must be at least 5 characters long")])
    email2 = StringField('Repeat Email', validators=[
                        DataRequired(), EqualTo('email'), Length(5, 128, "Email must be at least 5 characters long")])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(8, 32, "Password must be between 8 and 32 characters long")])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password'), Length(8, 32)])
    submit = SubmitField('Register')

    def validate_username(self, username) -> None:
        '''
        Validate a provided username
        
        It must not be taken already, and it must not be a blacklisted username

        :param username: Username to validate
        
        :return: None
        '''
        # Check if username is taken or is a blacklisted username
        if User.query.filter_by(username=username.data.lower()).first() or username.data.lower() in blacklisted_usernames:
            raise ValidationError("Username taken")

        # Check if username is valid with regex
        username_regex_check(username)

    def validate_email(self, email) -> None:
        '''
        Validate a provided email

        It must not be taken already

        :param email: Email to validate

        :return: None
        '''
        # Check if email is taken
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email taken")


class PostForm(FlaskForm):
    '''
    Form for creating a post

    Attributes:
        title (StringField): Title field
        body (TextAreaField): Body field
        submit (SubmitField): Submit button
    '''
    subject = StringField("Subject", validators=[
                          DataRequired(), Length(1, 128)])
    body = TextAreaField("Body", validators=[DataRequired(), Length(1, 3500)])
    submit = SubmitField("Submit")


class AdminSQLForm(FlaskForm):
    '''
    Form for submitting a form as admin

    Attributes:
        query (TextAreaField): Query field
        submit (SubmitField): Submit button
    '''
    query = TextAreaField("Query", validators=[DataRequired()])
    submit = SubmitField("Submit")


class EmptyForm(FlaskForm):
    '''
    Empty form with a submit button

    Attributes:
        submit (SubmitField): Submit button
    '''
    submit = SubmitField("Submit")


class EditProfileForm(FlaskForm):
    '''
    Form for editing a profile

    Attributes:
        username (StringField): Username field
        bio (TextAreaField): Bio field
        submit (SubmitField): Submit button

    Methods:
        validate_username: Checks if username is taken
    '''
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 16)])
    bio = TextAreaField('Bio', validators=[Length(0, 512)])
    submit = SubmitField("Submit")

    def validate_username(self, username) -> None:
        '''
        Validate a provided username

        It must not be taken already, and it must not be a blacklisted username

        :param username: Username to validate
        
        :return: None
        '''

        # Check if the user exists
        user = User.query.filter_by(username=username.data.lower()).first()

        # Check if username is taken or is a blacklisted username
        if user and user.username != current_user.username or username.data.lower() in username.data.lower() in blacklisted_usernames:
            raise ValidationError("Username taken")

        # Check if username is valid with regex
        username_regex_check(username)


class ControllerForm(FlaskForm):
    '''
    Form for controlling the robot
    
    Attributes:
        controllerInput (StringField): Controller input field
        submit (SubmitField): Submit button
    '''
    controllerInput = StringField('Controller', validators=[DataRequired()])
    submit = SubmitField("Submit")


class ForgotPasswordForm(FlaskForm):
    '''
    Form for resetting a password
    
    Attributes:
        email (StringField): Email field
        submit (SubmitField): Submit button
    '''
    email = StringField('Email', validators=[
                        DataRequired(), Email("Email must be valid"), Length(5, 128, "Email must be at least 5 characters long")])
    submit = SubmitField("Submit")

class ResetPasswordForm(FlaskForm):
    '''
    Form for resetting a password

    Attributes:
        password (PasswordField): Password field
        password2 (PasswordField): Password confirmation field
        submit (SubmitField): Submit button
    '''
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(8, 32, "Password must be between 8 and 32 characters long")])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password'), Length(8, 32)])
    submit = SubmitField('Reset Password')

class CommentForm(FlaskForm):
    '''
    Form for commenting on a post

    Attributes:
        comment (TextAreaField): Comment field
        submit (SubmitField): Submit button
    '''
    comment = TextAreaField("Comment", validators=[DataRequired(), Length(1, 1000)])
    submit = SubmitField("Submit")

def username_regex_check(username):
    '''
    Check if a username is valid with regex
    The username will only contain alphanumeric characters, underscores, dashes and full stops

    :param username: Username to check

    :return: None
    '''
    # Run regex check
    regex = re.compile(r"^[\-a-z0-9_\.]+$")

    # If there are no matches, raise error
    if not regex.match(username.data.lower()):
        raise ValidationError(
            "Invalid username. Username may not contain spaces or special characters besides '-', '_' & '.'")

# List of blacklisted usernames
global blacklisted_usernames
blacklisted_usernames = ['admin', 'moderator', 'owner', 'creator', 'mod', 'modteam', 'dev', 'developer', 'winston', 'winstogram', 'administrator']