import os

from flask import Flask, request, g

from flaskr.db import get_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
            )

    # SECRET_KEY
    # NEWS_API_KEY
    # API_KEY
    app.config.from_pyfile(
            os.path.join(app.instance_path, 'settings.cfg')
            )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hepitrack():
        return 'Welcome to Hepitrack'
    
    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import news
    app.register_blueprint(news.bp)
    
    return app
