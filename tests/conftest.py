import os
import tempfile
import json

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql=f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path=tempfile.mkstemp()

    app=create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client=client

    def login(self, email='test@hepitrack.com', password='test123456'):
        return self._client.post(
            '/auth/login',
            data=json.dumps(dict(email='test@hepitrack.com', password='test123456')),
            content_type='application/json'
        )

    def register(self, email='test@hepitrack.com', password='test123456'):
        return self._client.post(
            '/auth/register',
            data=json.dumps(dict(email='test@hepitrack.com', password='test123456')),
            content_type='application/json'
    )

@pytest.fixture
def auth(client):
    return AuthActions(client)
