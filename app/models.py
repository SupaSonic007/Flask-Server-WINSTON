import json
from datetime import datetime
from hashlib import md5
from time import time

import jwt
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db


class User(db.Model, UserMixin):

    # Class native attributes
    # format <name> = db.Column(<data type>, <primary key?>, <unique?>, <index by value?>, <default value?>)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    time_created = db.Column(db.DateTime, default=datetime.utcnow())
    password_hashed = db.Column(db.String(128))
    bio = db.Column(db.String(512))
    admin = db.Column(db.Boolean, default=False)

    # Relationships to other tables

    # Collection to user relationship
    # 'cascade all, delete' means that if a user is deleted, all of the information about them is deleted
    collections = db.relationship(
        'Collection', backref='collection_author', cascade='all, delete', lazy='dynamic')
    
    # Post to user relationship
    posts = db.relationship('Post', backref='author',
                            cascade='all, delete', lazy='dynamic')
    
    # Comment to user relationship
    comments = db.relationship(
        'Comment', backref='author', cascade='all, delete', lazy='dynamic')

    # Methods
    def __repr__(self) -> str:
        '''
        String representation of user
        
        :return: String representation of user
        '''
        return f"{self.username}"

    def __dir__(self) -> list:
        '''
        List of attributes of user

        :return: List of attributes of user
        '''
        return ['id', 'username', 'email', 'time_created', 'collections', 'posts']

    def set_password(self, password: str) -> None:
        '''
        Set the password of the user

        :param password: Password to set

        :return: None
        '''

        # Generate a password hash with sha256
        self.password_hashed = generate_password_hash(
            password, method="sha256")

        return

    def check_password(self, password):
        '''
        Check if the password provided matches the hashed password

        :param password: Password to check

        :return: True if the password matches, False if not
        '''

        return check_password_hash(self.password_hashed, password)

    def avatar(self, size):
        '''
        Get the avatar of the user

        :param size: Size of the avatar

        :return: Link to user avatar
        '''

        # md5 hash of username for gravatar
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()

        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def to_dict(self):
        """
        Convert user to dict
        
        :return: Dict of user without sensitive information
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
        '''
        Get a reset password token for the user
        
        :param expires_in: Time until the token expires
        
        :return: Reset password token
        '''
        
        # Encode payload with user id and expiration time (10 minutes) and secret key with the HS256 algorithm
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        '''
        Verify the reset password token provided

        :param token: Reset password token

        :return: User if the token is valid, None if not
        '''

        # Attempt to decode the jwt, if it fails it will error out and return None
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        
        return User.query.get(id)


class Post(db.Model, UserMixin):

    # Class Native attributes
    # format <name> = db.Column(<data type>, <primary key?>, <unique?>, <index by value?>, <default value?>)
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
        '''
        String representation of post
        
        :return: String representation of post
        '''
        return f"<Post {self.id} - {self.author}>"

    def __dir__(self) -> list:
        '''
        List of attributes of post

        :return: List of attributes of post
        '''
        return ['id', 'header', 'body', 'imageLocation', 'timestamp', 'user_id', 'collections']

    def to_dict(self):
        """
        Convert post to dict

        :return: Dict of post without sensitive information
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

        :return: String representation of post in json
        """
        return json.dumps(self.to_dict(), default=str)


class Collection(db.Model):

    # Class Native attributes
    # format <name> = db.Column(<data type>, <primary key?>, <unique?>, <index by value?>, <default value?>)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), default="New Collection")

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    posts = db.relationship('Post', secondary='collection_for_posts',
                            backref='collection_list', lazy='dynamic', cascade='all, delete')

    def __repr__(self) -> str:
        '''
        String representation of collection

        :return: String representation of collection
        '''
        return f"<Collection {self.id} - {self.collection_author}>"

    def __dir__(self) -> list:
        '''
        List of attributes of collection

        :return: List of attributes of collection
        '''
        return ['id', 'user_id', 'posts']

    def to_dict(self):
        """
        Convert collection to dict

        :return: Dict of collection without sensitive information
        """

        return {
            "id": self.id,
            "user_id": self.user_id,
            "posts": self.posts,
        }

    def to_json(self):
        """
        String representation of collection in json

        :return: String representation of collection in json
        """
        return json.dumps(self.to_dict(), default=str)


class CollectionForPosts(db.Model):

    # Relationships to other tables as this is a middle man for a many to many relationship
    collection_id = db.Column(db.Integer, db.ForeignKey(
        'collection.id', ondelete='CASCADE'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self) -> str:
        '''
        String representation of collection for posts
        
        :return: String representation of collection for posts
        '''
        return f"<CollectionForPosts {self.collection_id} - {self.post_id}>"

    def __dir__(self) -> list:
        '''
        List of attributes of collection for posts

        :return: List of attributes of collection for posts
        '''
        return ['collection_id', 'post_id']


class Comment(db.Model):
    # Class Native attributes
    # format <name> = db.Column(<data type>, <primary key?>, <unique?>, <index by value?>, <default value?>)
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'))

    def __repr__(self) -> str:
        '''
        String representation of comment

        :return: String representation of comment
        '''
        return f"<Comment {self.id} - {self.body}>"

    def __dir__(self) -> list:
        '''
        List of attributes of comment

        :return: List of attributes of comment
        '''
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
        '''
        String representation of like

        :return: String representation of like
        '''
        return f"<Like {self.id} - {self.user_id} - {self.post_id}>"

    def __dir__(self) -> list:
        '''
        List of attributes of like

        :return: List of attributes of like
        '''
        return ['id', 'timestamp', 'user_id', 'post_id']
