from app import app
from flask import render_template, flash, url_for, request

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
            'header': 'Epic',
            'body': 'Also epic',
            'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/182px-Python-logo-notext.svg.png'
        },
        {
            'header': 'Epic 2',
            'body': 'Also epic'
        },
        {
            'header': 'Epic',
            'body': 'Also epic'
        },
        {
            'header': 'Epic 2',
            'body': 'Also epic'
        },
        {
            'header': 'Epic',
            'body': 'Also epic'
        },
        {
            'header': 'Epic 2',
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