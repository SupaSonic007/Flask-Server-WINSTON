from app import app, db
from app.models import User, Post, Collection, CollectionForPosts, Comment, Like


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Collection': Collection, 'CollectionForPosts': CollectionForPosts, 'Comment': Comment, 'Like': Like}
