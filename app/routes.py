import json
import time

from flask import Response, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import text

from app import app, db
from app.email import send_password_reset_email
from app.forms import (AdminSQLForm, ControllerForm, EditProfileForm,
                       ForgotPasswordForm, LoginForm, PostForm,
                       RegistrationForm, ResetPasswordForm, CommentForm)
from app.models import (Collection, CollectionForPosts, Comment, Like, Post,
                        User)
from app.winston import sendToPi


def gen():
    
    while True:

        time.sleep(0.02)
        img = ""
        if open('D:/img_written.txt', 'r').read() == "1":
            img = open('D:/img.jpg', 'rb').read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
        
        elif open('D:/img_running.txt', 'r').read() == "0":
            img = open('app/static/images/placeholder.jpg', 'rb').read()
            return (b'--frame\r\n'
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


@app.route('/posts/<post_id>', methods=['GET', 'POST'])
@app.route('/posts', methods=['GET', 'POST'])
def winstogram(post_id=None):

    if post_id:
        comment_form = CommentForm()

        if comment_form.validate_on_submit():

            comment = Comment(
                body=comment_form.comment.data.replace(
                    '<', "&lt;").replace('>', "&gt;"),
                user_id=current_user.get_id(),
                post_id=post_id
            )

            db.session.add(comment)
            db.session.commit()

            return redirect(url_for('winstogram', post_id=post_id))

        post = Post.query.get_or_404(post_id)

        return render_template(
            'post.html',
            title='Post',
            current_user=current_user,
            id=post_id,
            authorid=post.user_id,
            app=app,
            form=comment_form
        )

    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(
            # Replace any attempted html injection with escaped characters
            header=post_form.subject.data.replace(
                '<', "&lt;").replace('>', "&gt;"),
            body=post_form.body.data.replace('\r', '').replace(
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
        current_user=current_user,
        app=app,
        form=post_form,
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
    
    # You can't view a user that doesn't exist
    user = User.query.get(id)

    if not user:
        return render_template(
            'errors/404.html',
            title='Page not found!',
            app=app
        ), 404

    return render_template(
        'user.html',
        title=f'{user.username}',
        user=id,
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

    collections = current_user.collections.all()
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

@app.route('/post/<id>/unsave', methods=["DELETE"])
def unsave_post(id):

    collections = current_user.collections
    if len(collections) == 0:
        collection = Collection(
            user_id=current_user.id
        )
        db.session.add(collection)
        db.session.commit()
    else:
        collection = current_user.collections[0]

    save_collection = CollectionForPosts.query.filter_by(
        collection_id=collection.id,
        post_id=int(id)
    ).first()

    if not save_collection:
        return {
            'status': 'error'
        }

    db.session.remove(save_collection)
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


@app.route('/stream_feed_left')
def stream_feed_left():
    if open('D:/img_running.txt', 'r').read() == '0':
        return (open('app/static/images/placeholder.jpg', 'rb').read())
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream_feed_right')
def stream_feed_right():
    if open('D:/img_running.txt', 'r').read() == '0':
        return (open('app/static/images/placeholder.jpg', 'rb').read())
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream_feed_processed')
def stream_feed_processed():
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

@app.route('/posts/saved')
def saved_posts():
    return render_template(
        'collections.html',
        title='Saved Posts',
        app=app,
        current_user=current_user
)

@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("No user found with that email")
            return redirect(url_for('forgot_password'))
        send_password_reset_email(user)
        flash("Password reset email sent! (Please check spam...)")
        return redirect(url_for('login'))

    return render_template(
        'forgot_password.html',
        title='Forgot Password',
        app=app,
        form=form
    )

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/mess_with_winston', methods=["GET", "POST"])
def mess_with_winston():
    return render_template(
        'mess_with_wint.html',
        title='Mess with Winston',
        app=app
    )