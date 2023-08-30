import json
from datetime import datetime
from hashlib import md5
from time import time

import jwt
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db


class User(db.Model, UserMixin):

    # Class native
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    time_created = db.Column(db.DateTime, default=datetime.utcnow())
    password_hashed = db.Column(db.String(128))
    bio = db.Column(db.String(512))
    admin = db.Column(db.Boolean, default=False)

    # Relationships
    collections = db.relationship(
        'Collection', backref='collection_author', cascade='all, delete', lazy='dynamic')
    posts = db.relationship('Post', backref='author',
                            cascade='all, delete', lazy='dynamic')
    comments = db.relationship(
        'Comment', backref='author', cascade='all, delete', lazy='dynamic')

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

    def to_dict(self):
        """
        Convert user to dict
        """

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "time_created": self.time_created,
            "bio": self.bio,
            "collections": self.collections,
            "posts": self.posts,

        }

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Post(db.Model, UserMixin):

    # Class Native
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(128))
    body = db.Column(db.String(2000))
    imageLocation = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationships
    comments = db.relationship(
        'Comment', backref='post', lazy='dynamic', cascade='all, delete')

    def __repr__(self) -> str:
        return f"<Post {self.id} - {self.author}>"

    def __dir__(self) -> list:
        return ['id', 'header', 'body', 'imageLocation', 'timestamp', 'user_id', 'collections']

    def to_dict(self):
        """
        Convert post to dict
        """

        return {
            "id": self.id,
            "header": self.header,
            "body": self.body,
            "imageLocation": self.imageLocation,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "collections": self.collections,
            "comments": self.comments,
        }

    def to_json(self):
        """
        String representation of post in json
        """
        return json.dumps(self.to_dict(), default=str)


class Collection(db.Model):

    # Class Native
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), default="New Collection")

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    posts = db.relationship('Post', secondary='collection_for_posts',
                            backref='collection_list', lazy='dynamic', cascade='all, delete')

    def __repr__(self) -> str:
        return f"<Collection {self.id} - {self.collection_author}>"

    def __dir__(self) -> list:
        return ['id', 'user_id', 'posts']

    def to_dict(self):
        """
        Convert collection to dict
        """

        return {
            "id": self.id,
            "user_id": self.user_id,
            "posts": self.posts,
        }

    def to_json(self):
        """
        String representation of collection in json
        """
        return json.dumps(self.to_dict(), default=str)


class CollectionForPosts(db.Model):

    # Relationships
    collection_id = db.Column(db.Integer, db.ForeignKey(
        'collection.id', ondelete='CASCADE'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self) -> str:
        return f"<CollectionForPosts {self.collection_id} - {self.post_id}>"

    def __dir__(self) -> list:
        return ['collection_id', 'post_id']


class Comment(db.Model):

    # Class Native
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'))

    def __repr__(self) -> str:
        return f"<Comment {self.id} - {self.body}>"

    def __dir__(self) -> list:
        return ['id', 'body', 'timestamp', 'user_id', 'post_id']


class Like(db.Model):

    # Class Native
    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'))

    def __repr__(self) -> str:
        return f"<Like {self.id} - {self.user_id} - {self.post_id}>"

    def __dir__(self) -> list:
        return ['id', 'timestamp', 'user_id', 'post_id']
