import os
from flask import Flask, request, g
from flaskr.db import get_db
from flask_cors import CORS

def create_app(test_config=None):
    app=Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
            )

    # SECRET_KEY
    # NEWS_API_KEY
    # API_KEY
    # SMTP_SERVER
    # SMTP_USER
    # SMTP_PASS
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
    from . import user
    app.register_blueprint(user.bp)
    from . import track
    app.register_blueprint(track.bp)

    CORS(app, resources={r'/*': {'origins': 'https://hepitrack.web.app'}})
    return app
