import time

from flask import Response, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import text

from app import app, db
from app.wrappers import admin_required
from app.email import send_password_reset_email
from app.forms import (AdminSQLForm, ControllerForm, EditProfileForm,
                       ForgotPasswordForm, LoginForm, PostForm,
                       RegistrationForm, ResetPasswordForm, CommentForm)
from app.models import (Collection, CollectionForPosts, Comment, Post,
                        User)
from app.winston import sendToPi


def gen():
    '''
    Generator function to stream the video feed

    A 'D: Drive' (D:/) WILL BE NEEDED FOR THIS TO WORK

    :return: The image frame
    '''
    while True:
        time.sleep(0.02)
        img = ""
        # Check if the image has been written from blender (without a camera feed, blender is used)
        if open('D:/img_written.txt', 'r').read() == "1":
            # Read the image and yield it
            img = open('D:/img.jpg', 'rb').read()
            
            # Send the frame of the image over the server
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

        elif open('D:/img_running.txt', 'r').read() == "0":
            # If the program isn't running, send a placeholder image
            img = open('app/static/images/placeholder.jpg', 'rb').read()
            return (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

        else:
            # If for some reason everything's broken, send a null frame
            yield (b'--frame\r\n')


@app.route('/')
@app.route('/index')
def index():
    '''
    Home Page

    :return: The rendered template
    '''
    return render_template(
        'index.html',
        title='Home',
        current_user=current_user,
        app=app
    )


@app.route('/about')
def about():
    '''
    About Us Page

    :return: The rendered template
    '''
    return render_template(
        'about.html',
        title='About',
        current_user=current_user,
        app=app
    )


@app.route('/posts/<post_id>', methods=['GET', 'POST'])
@app.route('/posts', methods=['GET', 'POST'])
def winstogram(post_id=None):
    '''
    Posts Page

    :param post_id: The id of the post to view

    :return: The rendered template
    '''
    # If a post has been selected to view, show it
    if post_id:
        # Setup comments
        comment_form = CommentForm()

        # If a comment has been submitted, add it to the database
        if comment_form.validate_on_submit():
            # Create a new comment, and replace any attempted html injection with escaped characters
            comment = Comment(
                body=comment_form.comment.data.replace(
                    '<', "&lt;").replace('>', "&gt;"),
                user_id=current_user.get_id(),
                post_id=post_id
            )

            db.session.add(comment)
            db.session.commit()

            # Reload the page to show updated comments
            return redirect(url_for('winstogram', post_id=post_id))

        # Get the post from the database or 404
        post = Post.query.get_or_404(post_id)

        # Return the post page with the post and comments
        return render_template(
            'post.html',
            title='Post',
            current_user=current_user,
            id=post_id,
            authorid=post.user_id,
            app=app,
            form=comment_form
        )

    # On the post page, there is a form to create a post
    post_form = PostForm()
    # If you're creating a post, add it to the database
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
        # Reload the page to show the new post
        return redirect('posts')

    # Otherwise, if no forms being submitted, just show the posts page
    return render_template(
        'posts.html',
        title='Winstogram',
        current_user=current_user,
        app=app,
        form=post_form,
    )


@app.route('/stream')
def stream():
    '''
    Stream Page

    :return: The rendered template
    '''
    return render_template(
        'stream.html',
        title='Stream',
        user=current_user,
        app=app
    )


@app.route('/user/<id>')
def user(id=current_user.id if current_user else 1):
    '''
    User Page

    :param id: The id of the user to view

    :return: The rendered template
    '''

    # You can't view a user that doesn't exist
    user = User.query.get(id)
    if not user:
        abort(404)

    # Return the user page with the user
    return render_template(
        'user.html',
        title=f'{user.username}',
        user=id,
        current_user=current_user,
        app=app
    )


@app.route('/login', methods=["GET", "POST"])
def login():
    '''
    Login Page

    :return: The rendered template
    '''
    
    form = LoginForm()
    # If the form is submitted, try to log the user in
    if form.validate_on_submit():
        # If the user doesn't exist or the password is incorrect it will error
        user = User.query.filter_by(
            username=form.username.data.lower()).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        # Log the user in & redirect to home page
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
    '''
    Register Page

    :return: The rendered template
    '''

    form = RegistrationForm()

    # If the form is submitted, try to register the user
    if form.validate_on_submit():
        
        # If the user already exists, it will error
        user = User(username=form.username.data.lower(), email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Success! Welcome to Winstogram!')
        login_user(user=user)

        # Create a collection for saving posts for the user (default)
        collection = Collection(user_id=current_user.get_id())
        db.session.add(collection)
        db.session.commit()

        return redirect('/')

    # Otherwise, if no forms being submitted, just show the register page
    return render_template(
        'register.html',
        title=f'Register',
        form=form,
        app=app
    )


@app.route('/logout', methods=["POST"])
def logout():
    '''
    Logout Page

    :return: The home page
    '''

    logout_user()
    return redirect('/')


@app.route('/post/<id>/save', methods=["POST"])
def save_post(id):
    '''
    Save a post to a collection

    :param id: The id of the post to save

    :return: Request status
    '''

    # Get the user's collections
    collections = current_user.collections.all()

    # If the user doesn't have any collections, create one (Possibly made before the update to create a default collection)
    if len(collections) == 0:
        collection = Collection(
            user_id=current_user.id
        )
        db.session.add(collection)
        db.session.commit()
    else:
        # Select collection
        collection = current_user.collections[0]

    # Add the post to the collection
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
    '''
    Unsave a post from a collection

    :param id: The id of the post to unsave

    :return: Request status
    '''

    # Get the user's collections
    collections = current_user.collections

    # If the user doesn't have any collections, create one (Possibly made before the update to create a default collection), but this shouldn't run due to the save function preventing it
    if len(collections) == 0:
        collection = Collection(
            user_id=current_user.id
        )
        db.session.add(collection)
        db.session.commit()
    else:
        # Select collection
        collection = current_user.collections[0]

    # Check if the save exists
    save_collection = CollectionForPosts.query.filter_by(
        collection_id=collection.id,
        post_id=int(id)
    ).first()

    # If it doesn't exist, return an error
    if not save_collection:
        return {
            'status': 'error'
        }

    # Otherwise, delete the save
    db.session.remove(save_collection)
    db.session.commit()
    return {
        'status': 'success'
    }


@app.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    '''
    Edit Profile Page

    :return: The rendered template
    '''

    # Create the form
    form = EditProfileForm()

    # If the form is being submitted, update the user's profile
    if form.validate_on_submit():
        current_user.username = form.username.data.lower()
        current_user.bio = form.bio.data
        db.session.commit()
        flash("Profile updated!")
        
        # Redirect back to the user page
        return redirect(url_for('user', id=current_user.id))
    
    # Otherwise, if no forms being submitted, just show the edit profile page with a form filled with the user's current details
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
    '''
    Stream feed for the left camera

    :return: The image frame
    '''
    # As the data hasn't been registered yet from the pi, it will return the stream shown earlier
    if open('D:/img_running.txt', 'r').read() == '0':
        # If it isn't running, send a placeholder
        return (open('app/static/images/placeholder.jpg', 'rb').read())
    # Otherwise, start the stream
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream_feed_right')
def stream_feed_right():
    '''
    Stream feed for the right camera

    :return: The image frame
    '''
    # As the data hasn't been registered yet from the pi, it will return the stream shown earlier    
    if open('D:/img_running.txt', 'r').read() == '0':
        # If it isn't running, send a placeholder
        return (open('app/static/images/placeholder.jpg', 'rb').read())
    # Otherwise, start the stream
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream_feed_processed')
def stream_feed_processed():
    '''
    Stream feed for the processed image

    :return: The image frame
    '''
    # As the data hasn't been registered yet from the pi, it will return the stream shown earlier
    if open('D:/img_running.txt', 'r').read() == '0':
        # If it isn't running, send a placeholder
        return (open('app/static/images/placeholder.jpg', 'rb').read())
    # Otherwise, start the stream
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/posts/saved')
def saved_posts():
    '''
    Saved Posts Page

    :return: The rendered template
    '''

    return render_template(
        'collections.html',
        title='Saved Posts',
        app=app,
        current_user=current_user
    )


@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    '''
    Forgot password page

    :return: The rendered template
    '''

    # Make sure the user isn't logged in trying to get their password
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Create the form
    form = ForgotPasswordForm()

    # If the form is submitted, send the password reset email
    if form.validate_on_submit():

        # Find the user
        user = User.query.filter_by(email=form.email.data).first()

        # If the user doesn't exist, error out
        if not user:
            flash("No user found with that email")
            return redirect(url_for('forgot_password'))
        
        # Otherwise, send the email, it is frequently sent to spam so a message is shown to the user
        send_password_reset_email(user)
        flash("Password reset email sent! (Please check spam...)")
        
        return redirect(url_for('login'))

    # Otherwise, if no forms being submitted, just show the forgot password page
    return render_template(
        'forgot_password.html',
        title='Forgot Password',
        app=app,
        form=form
    )


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    '''
    Reset Password page

    :param token: The token to verify the user

    :return: The rendered template
    '''
    if current_user.is_authenticated:
        # If the user is logged in, redirect to home page
        return redirect(url_for('index'))
    
    # Verify the token
    user = User.verify_reset_password_token(token)

    # If the token is invalid, error out
    if not user:
        return redirect(url_for('index'))
    
    # Otherwise, create the form
    form = ResetPasswordForm()

    # If the form is submitted, reset the password
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        
        # Redirect to login page
        return redirect(url_for('login'))
    
    # Otherwise, if no forms being submitted, just show the reset password page
    return render_template('reset_password.html', form=form)


@app.route('/mess_with_winston', methods=["GET", "POST"])
def mess_with_winston():
    '''
    Mess with Winston page

    :return: The rendered template
    '''
    return render_template(
        'mess_with_wint.html',
        title='Mess with Winston',
        app=app
    )


@app.route('/collection/<id>')
@login_required
def collection(id):
    '''
    Collection page

    :param id: The id of the collection to view

    :return: The rendered template
    '''

    # Get the collection from the database or 404
    collection = Collection.query.get_or_404(id)

    # If the collection doesn't belong to the user, 401
    if current_user.id != collection.user_id:
        abort(401)

    return render_template(
        'collection.html',
        title=f'Collection {collection.name}',
        app=app,
        id=id,
    )


@app.route('/admin', methods=["POST", "GET"])
@admin_required
def admin():
    '''
    Admin page (Very important page)
    [ADMIN REQUIRED]

    :return: The rendered template
    '''

    # SQL Form for executing SQL statements
    sql_form = AdminSQLForm()

    # If the form is submitted, execute the SQL statement
    if sql_form.validate_on_submit():

        sql = sql_form.query.data

        # Execute SQL Statement, must be converted to SQL text to execute
        results = db.session.execute(text(sql))
        # commit if changing any values
        db.session.commit()

        # These do not return a result, therefore say they have been executed
        if 'delete' in sql.lower() or 'update' in sql.lower() or 'insert' in sql.lower():
            flash(f"Executed: {text(sql)}")
            return redirect('admin')
        else:
            # Otherwise, return the results of the query
            results = [tuple(row) for row in results.all()]
            flash((results))
            return redirect('admin')
        
    # Otherwise, if no forms being submitted, just show the admin page
    return render_template(
        'admin.html',
        title=f"Admin Panel",
        app=app,
        form=sql_form,
    )


@app.route('/admin/control', methods=["GET", "POST"])
@admin_required
def controller():
    '''
    Admin Control Page
    [ADMIN REQUIRED]

    :return: The rendered template
    '''

    # If the form is submitted, send the data to the pi
    # NOTE: The page only sends post requests and doesn't validate_on_submit for a more seamless experience
    if request.method == "POST":
        data = request.json['data']
        sendToPi(data)
        return "", 200

    # Otherwise, if no forms being submitted, just show the controller page
    form = ControllerForm()
    return render_template(
        'controller.html',
        title='Controller',
        app=app,
        form=form
    )


@app.route('/test')
@admin_required
def test():
    '''
    Test Page for any features being tested
    [ADMIN REQUIRED]

    :return: The rendered template
    '''
    return render_template(
        'TEST.html',
        title='Test',
        app=app
    )
