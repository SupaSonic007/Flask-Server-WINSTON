from app import app, db
from flask import render_template, flash, url_for, request, redirect
from app.forms import LoginForm, RegistrationForm, LogoutForm
from app.models import User, Post
from flask_login import login_user, current_user, login_required, logout_user

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', current_user=current_user, app=app)

@app.route('/about')
def about():
    return render_template('about.html', title='About', current_user=current_user, app=app)

@app.route('/post')
@app.route('/posts')
def winstogram():

    # Dummy data
    posts = [
        {
            'head': 'Epic',
            'body': 'Also epic',
            'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/182px-Python-logo-notext.svg.png'
        },
        {
            'head': 'Epic 2',
            'body': 'Also epic'
        },
        {
            'head': 'Epic',
            'body': 'Also epic'
        },
        {
            'head': 'Epic 2',
            'body': 'Also epic'
        },
        {
            'head': 'Epic',
            'body': 'Also epic'
        },
        {
            'head': 'Epic 2',
            'body': 'Also epic'
        },
    ]

    return render_template('posts.html', title='Winstogram', posts=posts, current_user=current_user, app=app)

@app.route('/stream')
def stream():
    return render_template('stream.html', title='Stream', user=current_user, app=app)

@app.route('/user/<id>')
def user(id=current_user.id if current_user else 1):
    user = User.query.get(id)
    if not user: return(render_template('errors/404.html', title='Page not found!'))
    
    return render_template('user.html', title=f'{user.username}', user=user, current_user=current_user, app=app)


@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user=user, remember=form.remember_me.data)
        flash(f"Welcome back, {user.username}")
        return redirect('/')


    return render_template('login.html', title=f'Login', form=form, app=app)

@app.route('/register', methods=["GET", "POST"])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Success! Congrats on becoming a WinStoner!')
        login_user(user=user)
        return redirect('/')

    return render_template('register.html', title=f'Register', form=form, app=app)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/admin')
def admin():
    if current_user.email in app.config['ADMINS']: return render_template('admin.html', title=f"Admin Panel", app=app)
    return(render_template('errors/404.html', title='Page not found!'))