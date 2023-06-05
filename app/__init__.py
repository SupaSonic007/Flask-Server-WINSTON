from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'
login.login_message = 'Please log in to access this page.'
moment = Moment(app)

from app import routes, models, errors

@login.user_loader
def load_user(user):
    return models.User.query.get(user)