import time

from flask import Response, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import text

from app import app, db
from app.forms import (AdminSQLForm, EditProfileForm, LoginForm, PostForm,
                       RegistrationForm, SaveForm, ControllerForm)
from app.models import Collection, CollectionForPosts, Post, User, Comment, Like
from app.winston import sendToPi

import json


def gen():
    while True:

        time.sleep(0.02)
        img = ""
        if open('D:/img_written.txt', 'r').read() == "1":
            img = open('D:/img.jpg', 'rb').read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
        else:
            yield (b'--frame\r\n')


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        title='Home',
        current_user=current_user,
        app=app
    )


@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About',
        current_user=current_user,
        app=app
    )


@app.route('/posts/<id>', methods=['GET', 'POST'])
@app.route('/posts', methods=['GET', 'POST'])
def winstogram(id=None):

    # For pagination, get page number from url (not being provided yet but will be in the future)
    page = request.args.get('page', 1, type=int)
    posts = []

    if id:
        form = SaveForm()
        if form.validate_on_submit():
            # Save the post
            saveCollection = current_user.collections.first()
            saveCollection.posts.append(Post.query.get(id))
            db.session.commit()

            return redirect(url_for('post', id=id))
        return render_template(
            'post.html',
            title='Post',
            post=Post.query.get(id),
            author=User.query.get(Post.query.get(id).user_id),
            current_user=current_user,
            app=app,
            form=form
        )

    for post in Post.query.paginate(page=page, per_page=10, error_out=False).items:
        # Replace any attempted html injection with escaped characters
        posts.append({
            'header': post.header.replace('<', "&lt;").replace('>', "&gt;"),
            'body': post.body.replace('\n', ' ').replace('<', "&lt; ").replace('>', "&gt; "),
            'author': User.query.get(Post.query.get(post.id).user_id).username,
            'id': post.id,
            'timestamp': post.timestamp
        })

    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            # Replace any attempted html injection with escaped characters
            header=form.subject.data.replace(
                '<', "&lt;").replace('>', "&gt;"),
            body=form.body.data.replace('\r', '').replace(
                '<', "&lt;").replace('>', "&gt;"),
            imageLocation=None,
            user_id=current_user.get_id()
        )
        # Add post to database
        db.session.add(post)
        db.session.commit()
        return redirect('posts')

    return render_template(
        'posts.html',
        title='Winstogram',
        posts=json.dumps(posts, default=str),
        current_user=current_user,
        app=app,
        form=form,
        page=page
    )


@app.route('/stream')
def stream():
    return render_template(
        'stream.html',
        title='Stream',
        user=current_user,
        app=app
    )


@app.route('/user/<id>')
def user(id=current_user.id if current_user else 1):
    user = User.query.get(id)
    # You can't view a user that doesn't exist
    if not user:
        return render_template(
            'errors/404.html',
            title='Page not found!',
            app=app
        )

    return render_template(
        'user.html',
        title=f'{user.username}',
        user=user,
        current_user=current_user,
        app=app
    )


@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # If the user doesn't exist or the password is incorrect it will error
        user = User.query.filter_by(
            username=form.username.data.lower()).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user=user, remember=form.remember_me.data)
        flash(f"Welcome back, {user.username}")
        return redirect('/')

    return render_template(
        'login.html',
        title=f'Login',
        form=form,
        app=app
    )


@app.route('/register', methods=["GET", "POST"])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Success! Welcome to Winstogram!')
        login_user(user=user)

        # Create a collection for saving for the user (default)
        collection = Collection(user_id=current_user.get_id())
        db.session.add(collection)
        db.session.commit()
        return redirect('/')

    return render_template(
        'register.html',
        title=f'Register',
        form=form,
        app=app
    )


@app.route('/logout', methods=["POST"])
def logout():
    # Log out the user, it will only be POST to
    logout_user()
    return redirect('/')


@app.route('/admin', methods=["POST", "GET"])
@login_required
def admin():
    if current_user.email in app.config['ADMINS']:

        sql_form = AdminSQLForm()
        tables = list(db.metadata.tables.keys())
        tableModels = {"user": User, "post": Post, "collection": Collection,
                       "collection_for_posts": CollectionForPosts}

        table = None
        view = None
        collection = None
        post = None
        selection = None
        # Inspect a database entry
        if request.args.listvalues():
            table = request.args.get('table')
            view = request.args.get('view')
            collection = request.args.get('collection')
            post = request.args.get('post')

            if table == 'collection_for_posts':
                selection = tableModels[table].query.filter(
                    tableModels[table].collection_id == collection).filter(tableModels[table].post_id == post).first()
            else:
                selection = tableModels[table].query.filter(
                    tableModels[table].id == view).first()

        if sql_form.validate_on_submit():
            sql = sql_form.query.data

            # Execute SQL Statement, must be converted to SQL text to execute
            results = db.session.execute(text(sql))
            # commit if changing any values
            db.session.commit()

            # Delete does not return a result
            if 'delete' in sql.lower():
                flash(f"Executed: {text(sql)}")
                return redirect('admin')
            else:
                results = [tuple(row) for row in results.all()]
                flash((results))
                return redirect('admin')
        columns = dir(selection)
        return render_template(
            'admin.html',
            title=f"Admin Panel",
            app=app,
            form=sql_form,
        )
    return render_template(
        'errors/404.html',
        title='Page not found!',
        app=app
    ), 404


@app.route('/post/<id>/save', methods=["POST"])
def save_post(id):

    collections = current_user.collections
    if len(collections) == 0:
        collection = Collection(
            user_id=current_user.id
        )
        db.session.add(collection)
        db.session.commit()
    else:
        collection = current_user.collections[0]

    save_collection = CollectionForPosts(
        collection_id=collection.id,
        post_id=int(id)
    )

    db.session.add(save_collection)
    db.session.commit()
    return {
        'status': 'success'
    }


@app.route('/edit_profile', methods=["GET", "POST"])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data.lower()
        current_user.bio = form.bio.data
        db.session.commit()
        flash("Profile updated!")
        return redirect(url_for('user', id=current_user.id))
    form.username.data = current_user.username
    form.bio.data = current_user.bio
    return render_template(
        'edit_profile.html',
        title='Edit Profile',
        form=form,
        app=app
    )


@app.route('/stream_feed')
def stream_feed():
    if open('D:/img_running.txt', 'r').read() == '0':
        return (open('app/static/images/placeholder.jpg', 'rb').read())
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/admin/control', methods=["GET", "POST"])
@login_required
def controller():

    if request.method == "POST":
        data = request.json['data']
        sendToPi(data)
        return "", 200

    form = ControllerForm()
    if current_user.email in app.config['ADMINS']:
        return render_template(
            'controller.html',
            title='Controller',
            app=app,
            form=form
        )
    return render_template(
        'errors/404.html',
        title='Page not found!',
        app=app
    ), 404