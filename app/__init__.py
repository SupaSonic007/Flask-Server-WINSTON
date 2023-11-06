from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import MetaData

from config import Config

# For updating migrations, conventions must be used or errors will occur
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

# Create the Flask app
app = Flask(__name__)

# Configure the Flask app
app.config.from_object(Config)

# Load the database
db = SQLAlchemy(app, metadata=metadata)

# Create the database migration engine
migrate = Migrate(app, db, render_as_batch=True)

# Create the login manager
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'
login.login_message = 'Please log in to access this page.'

# Create the moment object (time manager)
moment = Moment(app)

# Create the mail object
mail = Mail(app)

# Import other parts of the app
from app import api, errors, models, routes, winston, wrappers

# Create the user loader
@login.user_loader
def load_user(user):
    return models.User.query.get(user)
