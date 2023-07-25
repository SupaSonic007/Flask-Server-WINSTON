from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    time_created = db.Column(db.DateTime, default=datetime.utcnow())
    password_hashed = db.Column(db.String(128))
    bio = db.Column(db.String(512))
    collections = db.relationship(
        'Collection', backref='collection_author')
    posts = db.relationship('Post', backref='author')

    def __repr__(self) -> str:
        return f"{self.username}"

    def __dir__(self) -> list:
        return ['id', 'username', 'email', 'time_created', 'collections', 'posts']

    def set_password(self, password: str) -> None:

        self.password_hashed = generate_password_hash(
            password, method="sha256")

        return

    def check_password(self, password):

        return check_password_hash(self.password_hashed, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Post(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(128))
    body = db.Column(db.String(2000))
    imageLocation = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    collections = db.relationship('Collection', secondary='collection_for_posts', backref=db.backref(
        'post_list'))

    def __repr__(self) -> str:
        return f"<Post {self.id} - {self.author}>"

    def __dir__(self) -> list:
        return ['id', 'header', 'body', 'imageLocation', 'timestamp', 'user_id', 'collections']


class Collection(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = db.relationship('Post', secondary='collection_for_posts', backref=db.backref(
        'collection_list'))

    def __repr__(self) -> str:
        return f"<Collection {self.id} - {self.collection_author}>"

    def __dir__(self) -> list:
        return ['id', 'user_id', 'posts']


class CollectionForPosts(db.Model):

    collection_id = db.Column(db.Integer, db.ForeignKey(
        'collection.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)

    def __repr__(self) -> str:
        return f"<CollectionForPosts {self.collection_id} - {self.post_id}>"

    def __dir__(self) -> list:
        return ['collection_id', 'post_id']

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self) -> str:
        return f"<Comment {self.id} - {self.body}>"

    def __dir__(self) -> list:
        return ['id', 'body', 'timestamp', 'user_id', 'post_id']
    
class Like(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self) -> str:
        return f"<Like {self.id} - {self.user_id} - {self.post_id}>"

    def __dir__(self) -> list:
        return ['id', 'timestamp', 'user_id', 'post_id']