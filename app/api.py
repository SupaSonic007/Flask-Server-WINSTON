import json

from flask import request, jsonify

from app import app
from app.models import Collection, Comment, Post, User


@app.route('/api', methods=["POST"])
def api():
    return jsonify(response="Invalid request", status="error"), 400


@app.route('/api/posts', methods=["POST"])
def api_posts():
    """
    Get post by id
    """
    data = request.get_json()

    if not data or not data.get('id'):
        return jsonify(response="Invalid request", status='error'), 400

    post = Post.query.get(data.get('id'))

    if not post:
        return jsonify(response="Post not found", status='error'), 404

    response = {
        'id': post.id,
        'subject': post.subject,
        'body': post.body,
        'timestamp': post.timestamp,
        'user_id': post.user_id,
        'comments': {
            comment.id: {
                'id': comment.id,
                'body': comment.body,
                'timestamp': comment.timestamp,
                'user_id': comment.user_id,
                'post_id': comment.post_id,
            } for comment in post.comments.all()
        },
    }

    return jsonify(**response), 200


@app.route('/api/posts/all', methods=["POST"])
def api_posts_all():
    """
    Get all posts
    """

    posts = Post.query.all()

    response = {
        'posts': {
            post.id: {
                'id': post.id,
                'subject': post.subject,
                'body': post.body,
                'timestamp': post.timestamp,
                'user_id': post.user_id,
                'comments': {
                    comment.id: {
                        'id': comment.id,
                        'body': comment.body,
                        'timestamp': comment.timestamp,
                        'user_id': comment.user_id,
                        'post_id': comment.post_id,
                    } for comment in post.comments.all()
                }
            } for post in posts
        }
    }, 200

    return jsonify(**response), 200


@app.route('/api/users', methods=["POST"])
def api_users():
    """
    Get user by id
    """

    data = request.get_json()

    if not data or not data.get('id'):
        return jsonify(response="Invalid request", status='error'), 400

    user = User.query.get(data.get('id'))

    if not user:
        return jsonify(response="User not found", status='error'), 404

    response = {
        'id': user.id,
        'username': user.username,
        'posts': {
            post.id: {
                'id': post.id,
                'subject': post.subject,
                'body': post.body,
                'timestamp': post.timestamp,
                'user_id': post.user_id,
                'comments': {
                    comment.id: {
                        'id': comment.id,
                        'body': comment.body,
                        'timestamp': comment.timestamp,
                        'user_id': comment.user_id,
                        'post_id': comment.post_id,
                    } for comment in post.comments.all()
                },
            } for post in user.posts.all()
        },
        'comments': {
            comment.id: {
                'id': comment.id,
                'body': comment.body,
                'timestamp': comment.timestamp,
                'user_id': comment.user_id,
                'post_id': comment.post_id,
            } for comment in user.comments.all()
        }
    }, 200

    return jsonify(**response), 200


@app.route('/api/users/all', methods=["POST"])
def api_users_all():
    """
    Get all users
    """

    users = User.query.all()

    response = {
        'users':
        {
            user.id:
            {
                'id': user.id,
                'username': user.username,
                'posts':
                {
                    post.id:
                    {
                        'id': post.id,
                        'subject': post.subject,
                        'body': post.body,
                        'timestamp': post.timestamp,
                        'user_id': post.user_id,
                        'comments':
                        {
                            comment.id:
                            {
                                'id': comment.id,
                                'body': comment.body,
                                'timestamp': comment.timestamp,
                                'user_id': comment.user_id,
                                'post_id': comment.post_id,
                            } for comment in post.comments.all()
                        },
                    } for post in user.posts.all()
                },
                'comments':
                {
                    comment.id:
                    {
                        'id': comment.id,
                        'body': comment.body,
                        'timestamp': comment.timestamp,
                        'user_id': comment.user_id,
                        'post_id': comment.post_id,
                    } for comment in user.comments.all()
                },
            } for user in users
        },
    }
    return jsonify(**response), 200


@app.route('/api/collections', methods=["POST"])
def api_collections():
    """
    Get collection by id
    """

    data = request.get_json()

    if not data or not data.get('id'):
        return jsonify(response="Invalid request", status='error'), 400

    collection = Collection.query.get(data.get('id'))

    if not collection:
        return jsonify(response="Collection not found", status='error'), 404

    response = {
        'id': collection.id,
        'user_id': collection.user_id,
        'posts': {
            post.id: {
                'id': post.id,
                'subject': post.subject,
                'body': post.body,
                'timestamp': post.timestamp,
                'user_id': post.user_id,
                'comments': {
                    comment.id: {
                        'id': comment.id,
                        'body': comment.body,
                        'timestamp': comment.timestamp,
                        'user_id': comment.user_id,
                        'post_id': comment.post_id,
                    } for comment in post.comments.all()
                },
            } for post in collection.posts.all()
        },
    }
    return jsonify(**response), 200


@app.route('/api/collections/all', methods=["POST"])
def api_collections_all():
    """
    Get all collections
    """

    collections = Collection.query.all()

    response = {
        'collections': {
            collection.id: {
                'id': collection.id,
                'user_id': collection.user_id,
                'posts': {
                    post.id: {
                        'id': post.id,
                        'subject': post.subject,
                        'body': post.body,
                        'timestamp': post.timestamp,
                        'user_id': post.user_id,
                        'comments': {
                            comment.id: {
                                'id': comment.id,
                                'body': comment.body,
                                'timestamp': comment.timestamp,
                                'user_id': comment.user_id,
                                'post_id': comment.post_id,
                            } for comment in post.comments.all()
                        },
                    } for post in collection.posts.all()
                },
            } for collection in collections
        },
    }
    return jsonify(**response), 200


@app.route('/api/comments', methods=["POST"])
def api_comments():
    """
    Get comment by id
    """

    data = request.get_json()

    if not data or not data.get('id'):
        return jsonify(response="Invalid request", status='error'), 400

    comment = Comment.query.get(data.get('id'))

    if not comment:
        return jsonify(response="Comment not found", status='error'), 404

    response = {
        'id': comment.id,
        'body': comment.body,
        'timestamp': comment.timestamp,
        'user_id': comment.user_id,
        'post_id': comment.post_id,
    }
    return jsonify(**response), 200


@app.route('/api/comments/all', methods=["POST"])
def api_comments_all():
    """
    Get all comments
    """

    comments = Comment.query.all()

    response = {
        'comments': {
            comment.id: {
                'id': comment.id,
                'body': comment.body,
                'timestamp': comment.timestamp,
                'user_id': comment.user_id,
                'post_id': comment.post_id,
            } for comment in comments
        },
        'status': 'success',
    }
    return jsonify(**response), 200
