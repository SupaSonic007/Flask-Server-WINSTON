from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    '''
    Render the 404 (page not found) page

    :param error: Error

    :return: Rendered 404 page
    '''
    return render_template("errors/404.html", app=app), 404

@app.errorhandler(500)
def internal_error(error):
    '''
    Render the 500 (Internal Error) page
    
    :param error: Error

    :return: Rendered 500 page
    '''
    # Rollback the database to not have the error in it
    db.session.rollback()

    return render_template("errors/500.html", app=app), 500

@app.errorhandler(401)
def unauthorized_error(error):
    '''
    Render the 401 (Unauthorized) page

    :param error: Error

    :return: Rendered 401 page
    '''
    return render_template("errors/401.html", app=app), 401