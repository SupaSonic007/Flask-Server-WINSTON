import json
import re
from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


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
    comments = db.relationship('Comment', backref='author')

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


class Post(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(128))
    body = db.Column(db.String(2000))
    imageLocation = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    collections = db.relationship('Collection', secondary='collection_for_posts', backref=db.backref(
        'post_list'))
    comments = db.relationship('Comment', backref=db.backref('post'), lazy='dynamic')

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

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = db.relationship('Post', secondary='collection_for_posts', backref=db.backref(
        'collection_list'))

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
