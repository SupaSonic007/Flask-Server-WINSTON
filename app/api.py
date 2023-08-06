import json

from flask import request, jsonify

from app import app, db
from app.models import Collection, Comment, Post, User


@app.route('/api', methods=["GET"])
def api():
    """
    API root
    """
    return jsonify(response="Invalid request", status="error"), 400


@app.route('/api/posts/<id>', methods=["GET"])
def api_post(id):
    """
    Get post by id
    :param id: post id
    :return: json
    """

    if not id:
        return jsonify(response="Invalid request", status='error'), 400

    post = Post.query.get(id)

    if not post:
        return jsonify(response="Post not found", status='error'), 404

    response = {
        'id': post.id,
        'header': post.header,
        'body': post.body,
        'timestamp': post.timestamp,
        'username': post.author.username,
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

    return response, 200


@app.route('/api/posts', methods=["GET"])
def api_posts_all():
    """
    Get all posts
    :return: json
    """

    posts = Post.query.all()

    response = {
        'posts': {
            post.id: {
                'id': post.id,
                'header': post.header,
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

    return response, 200


@app.route('/api/users/<id>', methods=["GET"])
def api_users(id):
    """
    Get user by id
    :param id: user id
    :return: json
    """

    if not id:
        return jsonify(response="Invalid request", status='error'), 400

    user = User.query.get(id)

    if not user:
        return jsonify(response="User not found", status='error'), 404

    response = {
        'id': user.id,
        'username': user.username,
        'posts': {
            post.id: {
                'id': post.id,
                'header': post.header,
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

    return response, 200


@app.route('/api/users', methods=["GET"])
def api_users_all():
    """
    Get all users
    :return: json
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
                        'header': post.header,
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
    return response, 200


@app.route('/api/collections/<id>', methods=["GET"])
def api_collections(id):
    """
    Get collection by id
    :param id: collection id
    :return: json
    """

    if not id:
        return jsonify(response="Invalid request", status='error'), 400

    collection = Collection.query.get(id)

    if not collection:
        return jsonify(response="Collection not found", status='error'), 404

    response = {
        'id': collection.id,
        'user_id': collection.user_id,
        'posts': {
            post.id: {
                'id': post.id,
                'header': post.header,
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
    return response, 200


@app.route('/api/collections', methods=["GET"])
def api_collections_all():
    """
    Get all collections
    :return: json
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
                        'header': post.header,
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
    return response, 200


@app.route('/api/comments/<id>', methods=["GET"])
def api_comments(id):
    """
    Get comment by id
    :param id: comment id
    :return: json
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
    return response, 200


@app.route('/api/comments', methods=["GET"])
def api_comments_all():
    """
    Get comments
    :return: json
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
    return response, 200


@app.route('/api/latest_posts/', methods=["GET"])
def api_latest_posts():
    """
    Get latest posts
    :return: json
    """

    amount = request.args.get('amount', 5)
    offset = request.args.get('offset', None)

    if offset: offset = int(offset)
    print(offset, amount)
    if offset and offset != 1: offset = int(offset)+1
    elif offset == 1: amount = 0; offset = 0
    else: offset = 0
    print(offset, amount)

    # Get posts from db starting at offset (earliest loaded post ID) and going backwards
    posts = Post.query.order_by(Post.id.desc()).offset(offset).limit(amount).all()

    response = [{
            'id': post.id,
            'header': post.header,
            'body': post.body,
            'timestamp': post.timestamp,
            'username': post.author.username,
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
        } for post in posts
    ]
    return response, 200


@app.route('/api/check_existence_in_collections/<id>', methods=['GET'])
def api_check_existence_in_collections(id=None):
    """
    Check if a post is present in a collection
    :param id: post id
    :return: json
    """

    if not id:
        return jsonify(response="Invalid request", status='error'), 400

    if not Post.query.get(id):
        return jsonify(response="Post not found", status='error'), 404

    if db.session.query(Collection).filter(Collection.posts.any(id=id)).count() > 0:
        return jsonify(response=True, status='success'), 200

    return jsonify(response=False, status='success'), 200
