from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'
login.login_message = 'Please log in to access this page.'
moment = Moment(app)
mail = Mail(app)

from app import api, errors, models, routes, winston


@login.user_loader
def load_user(user):
    return models.User.query.get(user)