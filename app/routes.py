from app import app
from flask import render_template, flash, url_for, request

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home - W.I.N.S.T.O.N.')

@app.route('/about')
def about():
    return render_template('about.html', title='About - W.I.N.S.T.O.N.')

@app.route('/post')
@app.route('/posts')
def posts():
    return render_template('posts.html', title='Winstogram - W.I.N.S.T.O.N.')

@app.route('/stream')
def stream():
    return render_template('stream.html', title='Stream - W.I.N.S.T.O.N.')

@app.route('/user/<username>')
def user(username):

    # Database not setup yet but will use a query
    user = None 

    return render_template('user.html', title=f'{username} - W.I.N.S.T.O.N.', user=user)