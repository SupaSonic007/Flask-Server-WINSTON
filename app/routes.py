from app import app, db
from flask import render_template, flash, url_for, request, redirect
from markupsafe import escape
from app.forms import LoginForm, RegistrationForm, PostForm, AdminSQLForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user
from sqlalchemy import text
from json import dumps


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


@app.route('/post', methods=['GET','POST'])
@app.route('/posts', methods=['GET','POST'])
def winstogram():

    page = request.args.get('page', 1, type=int)
    # All posts for now
    posts = []
    form = PostForm()

    for post in Post.query.paginate(page=page, error_out=False).items:
        posts.append({
            'header': post.heading.replace(r'/</g', "&lt; ").replace(r'/>/g', "&gt; "),
            'body': post.body.replace('\n','<br>').replace(r'/</g', "&lt; ").replace(r'/>/g', "&gt; "),
            'author': post.user_id,
        })

    if form.validate_on_submit():
        post = Post(
            heading = form.subject.data.replace(r'/</g', "&lt;").replace(r'/>/g', "&gt;"),
            body = form.body.data.replace('\r','').replace(r'/</g', "&lt;").replace(r'/>/g', "&gt;"),
            imageLocation = None,
            user_id = current_user.get_id()
        )
        db.session.add(post)
        db.session.commit()
        return redirect('posts')
    
    return render_template(
        'posts.html',
        title='Winstogram',
        posts=posts,
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
        flash('Success! Congrats on becoming a WinStoner!')
        login_user(user=user)
        return redirect('/')

    return render_template(
        'register.html',
        title=f'Register',
        form=form,
        app=app
    )


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/admin', methods=["POST", "GET"])
def admin():
    if current_user.email in app.config['ADMINS']:
        
        sql_form = AdminSQLForm()
        tables = list(db.metadata.tables.keys())

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
            db=db,
            tableText="<br>".join(tables),
            tables=tables,
            tableModels={"user":User, "post":Post}
        )
    
    return render_template(
        'errors/404.html',
        title='Page not found!',
        app=app
        )
