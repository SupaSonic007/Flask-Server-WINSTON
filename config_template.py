import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # Create a key for the app
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Oh-beans-I-guess-this-key-isnt-very-secret"

    # Get the database if it exists or get the local app.db
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Setup mailing server
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""

    ADMINS = []

