from app import app, db
from app.models import User, Post, Collection, CollectionForPosts, Comment, Like

# For flask shell, create context
@app.shell_context_processor
def make_shell_context():
    '''
    Make the shell context
    
    :return: Shell context
    '''
    return {'db': db, 'User': User, 'Post': Post, 'Collection': Collection, 'CollectionForPosts': CollectionForPosts, 'Comment': Comment, 'Like': Like}
