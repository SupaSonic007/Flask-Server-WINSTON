from threading import Thread

from flask import render_template
from flask_mail import Message

from app import app, mail

def send_async_email(app, msg):
    '''
    Send an email asynchronously

    :param app: Flask app
    :param msg: Message to send

    :return: None
    '''
    with app.app_context():
        # Send the email
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    '''
    Send an email

    :param subject: Subject of the email
    :param sender: Sender of the email
    :param recipients: Recipients of the email
    :param text_body: Text body of the email
    :param html_body: HTML body of the email

    :return: None
    '''
    # Create the message object with flask_mail
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # Create another thread to send the email asynchronously
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
    '''
    Send a password reset email to a user

    :param user: User to send the email to

    :return: None
    '''
    # Generate a reset password token
    token = user.get_reset_password_token()
    # Define and send the email
    send_email('[Winstogram] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))