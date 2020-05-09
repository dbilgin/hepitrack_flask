import pytest
import json
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    register_response = client.post(
        '/auth/register',
        data=json.dumps(dict(email='test@test.com', password='test123456')),
        content_type='application/json'
    )
    assert register_response.status_code == 200
    assert b'access_token' in register_response.data

    with app.app_context():
        assert get_db().execute(
            "SELECT * from user where email = 'test@test.com'",
        ).fetchone() is not None

@pytest.mark.parametrize(('user_email', 'user_password', 'code'), (
    ('test', 'test', 400),
    ('a', None, 400),
    ('test@test.com', 'test9854', 409),
))
def test_login_validate_input(client, user_email, user_password, code):
    response = client.post(
        '/auth/register',
        data=json.dumps(dict(email=user_email, password=user_password)),
        content_type='application/json'

    )
    assert code == response.status_code

def test_login(client, auth, app):
    auth.register()
    
    login_response = client.post(
        '/auth/login',
        data=json.dumps(dict(email='test@test.com', password='test123456')),
        content_type='application/json'
    )
    assert login_response.status_code == 200
    assert b'access_token' in login_response.data

    with app.app_context():
        assert get_db().execute(
            "SELECT * from user where email = 'test@test.com'",
        ).fetchone() is not None


@pytest.mark.parametrize(('user_email', 'user_password', 'code'), (
    ('test', 'test', 400),
    ('a', None, 400),
    ('test@test.com', 'test123456', 200),
))
def test_login_validate_input(client, user_email, user_password, code):
    response = client.post(
        '/auth/register',
        data=json.dumps(dict(email=user_email, password=user_password)),
        content_type='application/json'

    )
    assert code == response.status_code
