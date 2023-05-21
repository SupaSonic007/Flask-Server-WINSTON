from app import app, db
from flask import render_template, flash, url_for, request, redirect
from app.forms import LoginForm, RegistrationForm
from app.models import User, Post

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/post')
@app.route('/posts')
def winstogram():
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
    return render_template('posts.html', title='Winstogram', posts=posts)

@app.route('/stream')
def stream():
    return render_template('stream.html', title='Stream')

@app.route('/user/<username>')
def user(username):

    # Database not setup yet but will use a query
    user = None 

    return render_template('user.html', title=f'{username}', user=user)

@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    return render_template('login.html', title=f'Login', form=form)

@app.route('/register', methods=["GET", "POST"])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Success! Congrats on becoming a WinStoner!')
        return redirect()

    return render_template('register.html', title=f'Register', form=form)