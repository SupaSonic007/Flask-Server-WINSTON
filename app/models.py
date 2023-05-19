from app import db
from datetime import datetime

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    timeCreated = db.Column(db.DateTime, default=datetime.utcnow())
    password_hashed = db.Column(db.String(128))

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    imageLocation = db.Column(db.String(64), unique=True)
    heading = db.Column(db.String(128), unique=True)
    heading = db.Column(db.String(2000), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f"<Post {self.id} - {self.author}>"