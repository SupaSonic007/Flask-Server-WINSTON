from sqlalchemy import text

from flask import request, jsonify
from flask_login import current_user, login_required

from app import app, db
from app.models import Collection, Comment, Post, User, CollectionForPosts, Like
from app.wrappers import admin_required


@app.route('/api', methods=["GET"])
def api():
    """
    API root

    The API root will return nothing

    :return: Response (json)
    """
    return jsonify(response="Invalid request", status="error"), 400


@app.route('/api/posts/<id>', methods=["GET"])
def api_post(id):
    """
    Get post by id

    :param id: post id

    :return: Response (json)
    """

    # If no id has been provided, throw an error
    if not id:
        return jsonify(response="Invalid request", status='error'), 400

    post = Post.query.get(id)

    # If the post doesn't exist, throw an error
    if not post:
        return jsonify(response="Post not found", status='error'), 404

    # Create the response with relevant data
    response = {
        'id': post.id,
        'header': post.header,
        'body': post.body,
        'timestamp': post.timestamp,
        'username': post.author.username,
        'user_id': post.user_id,
        'comments': [
            {
                'id': comment.id,
                'body': comment.body,
                'timestamp': comment.timestamp,
                'user_id': comment.user_id,
                'username': comment.author.username,
                'post_id': comment.post_id,
            } for comment in post.comments.all()
        ],
    }

    # Return the response with success status
    return response, 200


@app.route('/api/posts', methods=["GET"])
def api_posts_all():
    """
    Get all posts in the database

    :return: Response (json)
    """

    # Get all posts
    posts = Post.query.all()

    # Create the response with relevant data
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

    # Return the response with success status
    return response, 200


@app.route('/api/users/<id>', methods=["GET"])
def api_users(id):
    """
    Get user by id

    :param id: user id
    
    :return: Response (json)
    """

    # Get the avatar_size if it's been provided, otherwise default to 128
    avatar_size = request.args.get('avatar', 128)

    # If no id has been provided, throw an error
    if not id:
        return jsonify(response="Invalid request", status='error'), 400

    user = User.query.get(id)

    # If the user doesn't exist, throw an error
    if not user:
        return jsonify(response="User not found", status='error'), 404


    response = {
        'id': user.id,
        'username': user.username,
        'time_created': user.time_created,
        'bio': user.bio,
        'avatar': user.avatar(avatar_size or 128),
        'posts': [{
            'id': post.id,
            'header': post.header,
            'body': post.body,
            'timestamp': post.timestamp,
            'user_id': post.user_id,
            'username': post.author.username,
            'comments': {
                comment.id: {
                    'id': comment.id,
                    'body': comment.body,
                    'timestamp': comment.timestamp,
                    'user_id': comment.user_id,
                    'post_id': comment.post_id,
                } for comment in post.comments.all()
            },
        } for post in user.posts.all()],
        'comments': {
            comment.id: {
                'id': comment.id,
                'body': comment.body,
                'timestamp': comment.timestamp,
                'user_id': comment.user_id,
                'post_id': comment.post_id,
            } for comment in user.comments.all()
        }
    }

    # Return the response with success status
    return response, 200


@app.route('/api/users', methods=["GET"])
def api_users_all():
    """
    Get all users in the database

    :return: Response (json)
    """

    # Get all users
    users = User.query.all()

    # Create the response with relevant data
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

    # Return the response with success status
    return response, 200


@app.route('/api/collections/<id>', methods=["GET"])
def api_collections(id):
    """
    Get a collection by id

    :param id: collection id
    
    :return: Response (json)
    """

    # If no id has been provided, throw an error
    if not id:
        return jsonify(response="Invalid request", status='error'), 400

    collection = Collection.query.get(id)

    # If the collection doesn't exist, throw an error
    if not collection:
        return jsonify(response="Collection not found", status='error'), 404

    # Create the response with relevant data
    response = {
        'id': collection.id,
        'user_id': collection.user_id,
        'title': collection.name,
        'posts': [{
            'id': post.id,
            'header': post.header,
            'body': post.body,
            'timestamp': post.timestamp,
            'user_id': post.user_id,
            'author': post.author.username,
            'comments': [{
                comment.id: {
                    'id': comment.id,
                    'body': comment.body,
                    'timestamp': comment.timestamp,
                    'user_id': comment.user_id,
                    'post_id': comment.post_id,
                }
            } for comment in post.comments.all()],
        } for post in collection.posts.all()],
    }

    # Return the response with success status
    return response, 200


@app.route('/api/collections', methods=["GET"])
def api_collections_all():
    """
    Get all collections in the database

    :return: Response (json)
    """

    # Get all collections
    collections = Collection.query.all()

    # Create the response with relevant data
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

    # Return the response with success status
    return response, 200


@app.route('/api/user/collections/<id>', methods=["GET"])
def api_user_collections(id):
    """
    Get all collections of a user

    params: id - user id
    
    :return: Response (json)
    """

    # If no id has been provided, throw an error
    if not id:
        return jsonify(response="Invalid request", status='error'), 400

    # Get all collections of a user
    collections = Collection.query.filter_by(user_id=id).all()

    # Create the response with relevant data
    response = [
        {
            'id': collection.id,
            'user_id': collection.user_id,
            'username': collection.collection_author.username,
            'name': collection.name,
            'posts': [
                {
                    'id': post.id,
                    'header': post.header,
                    'body': post.body,
                    'timestamp': post.timestamp,
                    'user_id': post.user_id,
                } for post in collection.posts.all()
            ],
            'number_of_posts': len(collection.posts.all())
        } for collection in collections
    ]

    # Return the response with success status
    return response, 200


@app.route('/api/comments/<id>', methods=["GET"])
def api_comments(id):
    """
    Get comment by id
    :param id: comment id

    :return: Response (json)
    """

    data = request.get_json()

    # If no id has been provided, throw an error
    if not data or not data.get('id'):
        return jsonify(response="Invalid request", status='error'), 400

    comment = Comment.query.get(data.get('id'))

    # If the comment doesn't exist, throw an error
    if not comment:
        return jsonify(response="Comment not found", status='error'), 404

    # Create the response with relevant data
    response = {
        'id': comment.id,
        'body': comment.body,
        'timestamp': comment.timestamp,
        'user_id': comment.user_id,
        'post_id': comment.post_id,
    }

    # Return the response with success status
    return response, 200

@app.route('/api/comments', methods=["GET"])
def api_comments_all():
    """
    Get comments

    :return: Response (json)
    """

    # Get all comments
    comments = Comment.query.all()

    # Create the response with relevant data
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

    :return: Response (json)
    """

    # Get the amount of posts to return
    amount = request.args.get('amount', 5)

    # Specify which post you are loading before (e.g. load <amount> posts before <id> post)
    before = request.args.get('before', None)

    # Ensure before and amount exist
    if before:
        before = int(before)
    if before and before != 1:
        before -= 1
    elif before == 1:
        amount = 0
        before = 0
    else:
        # Check if there are posts, otherwise return nothing
        if Post.query.count():
            before = Post.query.order_by(Post.id.desc()).first().id
        else:
            return {}, 200

    # Get posts from db starting at before (earliest loaded post ID) and going backwards
    posts = Post.query.filter(Post.id <= before).order_by(
        Post.id.desc()).limit(amount).all()

    # Create the response with relevant data
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

    # Return the response with success status
    return response, 200


@app.route('/api/check_existence_in_collections/<id>', methods=['GET'])
def api_check_existence_in_collections(id=None):
    """
    Check if a post is present in a collection
    
    :param id: post id

    :return: Response (json)
    """

    # If no id has been provided, throw an error
    if not id:
        return jsonify(response="Invalid request", status='error'), 400

    # If the post doesn't exist, throw an error
    if not Post.query.get(id):
        return jsonify(response="Post not found", status='error'), 404

    # Check if the post is in any of the user's collections
    for collection in current_user.collections.all():
        if collection.posts.filter(Post.id == id).first():
            # Return the response with success status
            return jsonify(response=True, status='success'), 200

    # Return the response with success status
    return jsonify(response=False, status='success'), 200


@admin_required
@app.route('/api/table', methods=['GET'])
def api_table_data():
    """
    Get data for a table specified by table_name

    :return: Response (json)
    """

    # Table to get data from
    table_name = request.args.get('table_name', None)

    # Select option (e.g. count)
    select = request.args.get('select', None)

    # Ensure the table exists and that a select option has been provided
    if not table_name or not select:
        return jsonify(response="Invalid request", status='error'), 400

    # Specifying available options for future expansion
    select_options = ['count']

    # If the select option is valid, return the data
    if select:
        if select in select_options:

            match select:
                case 'count':
                    if table_name:
                        return db.session.query(table_name).count()
                    else:
                        tables = {
                            'user': User,
                            'post': Post,
                            'comment': Comment,
                            'collection': Collection,
                        }
                        return {table: tables[table].query.count() for table in list(tables.keys())}, 200

    # If the select option is not valid, return the table matching the table name
    match table_name:
        
        case 'user':
            users = User.query.all()
            # First Layer Data (user's immediate data, no recursion into other tables)
            response = [{
                user.id: {
                    'id': user.id,
                    'username': user.username,
                    'bio': user.bio,
                    'time_created': user.time_created,
                    'collections': [
                        collection.id for collection in user.collections.all()],
                    'posts': [
                        post.id for post in user.posts.all()],
                    'comments': [
                        comment.id for comment in user.comments.all()],
                    'admin': user.admin,
                },
            } for user in users]

            # Return the response with success status
            return response, 200

        case 'post':
            posts = Post.query.all()
            # First Layer Data (post's immediate data, no recursion into other tables)
            response = [{
                post.id: {
                    'id': post.id,
                    'header': post.header,
                    'body': post.body,
                    'timestamp': post.timestamp,
                    'user_id': post.user_id,
                    'username': post.author.username,
                    'comments': [comment.id for comment in post.comments.all()],
                }
            } for post in posts]

            # Return the response with success status
            return response, 200

        case 'comment':
            comments = Comment.query.all()
            # First Layer Data (post's immediate data, no recursion into other tables)
            response = [{
                comment.id: {
                    'id': comment.id,
                    'body': comment.body,
                    'timestamp': comment.timestamp,
                    'user_id': comment.user_id,
                    'post_id': comment.post_id,
                }
            } for comment in comments]

            # Return the response with success status
            return response, 200

        case 'collection':
            collections = Collection.query.all()
            # First Layer Data (post's immediate data, no recursion into other tables)
            response = [{
                collection.id: {
                    'id': collection.id,
                    'user_id': collection.user_id,
                    'posts': [post.id for post in collection.posts.all()]
                }
            } for collection in collections]

            # Return the response with success status
            return response, 200


@app.route('/api/camera_data/camera', methods=['GET', 'POST'])
def camera_data():
    """
    Send and receive camera data from the rpi

    :return: Response (json)
    """

    # If the request is a POST request, save the camera data to a file
    if request.method == 'POST':
        open('D:/camera_data_l.jpg',
             'wb').write(request.json['camera_data_left'].read().decode('utf-8'))
        open('D:/camera_data_r.jpg',
             'wb').write(request.json['camera_data_right'].read().decode('utf-8'))
        return 200

    # If the request is a GET request, return the camera data
    if request.method == 'GET':
        return {'left': open('D:/camera_data_l', 'rb').read(), 'right': open('D:/camera_data_r', 'rb').read()}, 200


@app.route('/api/camera_data/processed', methods=['POST'])
def processed_camera_data():
    """
    Send and receive processed camera data from another computer (or rpi)

    :return: Response (json)
    """

    # Save the processed camera data to a file
    open('D:/processed_camera_data',
         'wb').write(request.files['processed_camera_data'].read().decode('utf-8'))

    return 200

@login_required
@app.route('/api/database/update', methods=['PUT'])
def update_database_entry():
    '''
    Update a database entry
    
    :return: Response (json)
    '''
    # Get data from request
    data = request.get_json()
    table_name:str = data.get('table_name', None)
    entry_id:int = data.get('entry_id', None)
    new_data:dict = data.get('new_data', None)

    tables = {'user': User, 'post': Post, 'comment': Comment, 'collection': Collection}
    if not (current_user.admin or current_user.id == tables[table_name].query.get(entry_id).user_id):
        return jsonify(response="Unauthorized", status='error'), 401

    # Check if the request is valid
    if not (table_name and entry_id and new_data):
        return jsonify(response=f"Invalid request, missing table or entry: {table_name = }, {entry_id = }, {new_data = }", status='error'), 400

    # Go through each key in new_data and update the entry with the new value
    match table_name:

        case 'user':

            user = User.query.get(entry_id)

            # Ensure the user exists
            if not user:
                return jsonify(response="User not found", status='error'), 404

            # Update the value specified
            for key, value in new_data.items():
                match key:
                    case 'username':
                        user.username = value
                    case 'email':
                        user.email = value
                    case 'bio':
                        user.bio = value
                    case 'admin':
                        user.admin = value

            db.session.commit()

            # Return the response with success status
            return jsonify(response="User updated", status='success'), 200
        
        case 'post':

            post = Post.query.get(entry_id)

            # Ensure the post exists
            if not post:
                return jsonify(response="Post not found", status='error'), 404
            
            # Update the value specified
            for key, value in new_data.items():
                match key:
                    case 'header':
                        post.header = value
                    case 'body':
                        post.body = value
                    case 'imageLocation':
                        post.imageLocation = value

            db.session.commit()
            
            # Return the response with success status
            return jsonify(response="Post updated", status='success'), 200
        
        case 'comment':

            comment = Comment.query.get(entry_id)

            # Ensure the comment exists
            if not comment:
                return jsonify(response="Comment not found", status='error'), 404
            
            # Update the value specified
            for key, value in new_data.items():
                match key:
                    case 'body':
                        comment.body = value

            db.session.commit()

            # Return the response with success status
            return jsonify(response="Comment updated", status='success'), 200
        
        case 'collection':

            collection = Collection.query.get(entry_id)

            # Ensure the collection exists
            if not collection:
                return jsonify(response="Collection not found", status='error'), 404
            
            # Update the value specified
            for key, value in new_data.items():
                match key:
                    case 'name':
                        collection.name = value

            db.session.commit()

            # Return the response with success status
            return jsonify(response="Collection updated", status='success'), 200
        
        case _:
            # If the table name is invalid, return an error
            return jsonify(response="Invalid table name", status='error'), 400

@login_required
@app.route('/api/database/delete', methods=['DELETE'])
def delete_database_entry():
    '''
    Delete a database entry

    :return: Response (json)
    '''

    # Get data from request
    data = request.get_json()
    table_name = data.get('table_name', None)
    entry_id = data.get('entry_id', None)

    tables = {'user': User, 'post': Post, 'comment': Comment, 'collection': Collection}
    # IF you don't own the post, and you aren't an admin error out
    if not (current_user.admin or current_user.id == tables[table_name].query.get(entry_id).user_id):
        return jsonify(response="Unauthorized", status='error'), 401
    
    # Check if the request is valid
    if not (table_name and entry_id):
        return jsonify(response=f"Invalid request, missing table or entry: {table_name = }, {entry_id = }", status='error'), 400
    
    match table_name:

        case 'user':
            
            user = User.query.get(entry_id)

            # Ensure the user exists
            if not user:
                return jsonify(response="User not found", status='error'), 404
            
            # Delete the user
            db.session.delete(user)
            db.session.commit()

            # Return the response with success status
            return jsonify(response="User deleted", status='success'), 200
        
        case 'post':

            post = Post.query.get(entry_id)

            # Ensure the post exists
            if not post:
                return jsonify(response="Post not found", status='error'), 404
            
            # Delete the post
            db.session.delete(post)
            db.session.commit()

            # Return the response with success status
            return jsonify(response="Post deleted", status='success'), 200
        
        case 'comment':

            comment = Comment.query.get(entry_id)

            # Ensure the comment exists
            if not comment:
                return jsonify(response="Comment not found", status='error'), 404
            
            # Delete the comment
            db.session.delete(comment)
            db.session.commit()

            # Return the response with success status
            return jsonify(response="Comment deleted", status='success'), 200
        
        case 'collection':

            collection = Collection.query.get(entry_id)

            # Ensure the collection exists
            if not collection:
                return jsonify(response="Collection not found", status='error'), 404
            
            # Delete the collection
            db.session.delete(collection)
            db.session.commit()

            # Return the response with success status
            return jsonify(response="Collection deleted", status='success'), 200
        
        case _:
            # If the table name is invalid, return an error
            return jsonify(response="Invalid table name", status='error'), 400