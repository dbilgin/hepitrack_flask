import pytest
import json
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    register_response = client.post(
        '/auth/register',
        data=json.dumps(dict(email='test@hepitrack.com', password='test123456')),
        content_type='application/json'
    )
    assert register_response.status_code == 200
    assert b'access_token' in register_response.data

    with app.app_context():
        assert get_db().execute(
            "SELECT * from user where email = 'test@hepitrack.com'",
        ).fetchone() is not None

@pytest.mark.parametrize(('user_email', 'user_password', 'code'), (
    ('test', 'test', 400),
    ('a', None, 400),
    ('test@hepitrack.com', 'test9854', 409),
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
        data=json.dumps(dict(email='test@hepitrack.com', password='test123456')),
        content_type='application/json'
    )
    assert login_response.status_code == 200
    assert b'access_token' in login_response.data

    with app.app_context():
        assert get_db().execute(
            "SELECT * from user where email = 'test@hepitrack.com'",
        ).fetchone() is not None


@pytest.mark.parametrize(('user_email', 'user_password', 'code'), (
    ('test', 'test', 400),
    ('a', None, 400),
    ('test@hepitrack.com', 'test123456', 200)
))
def test_login_validate_input(client, user_email, user_password, code):
    response = client.post(
        '/auth/register',
        data=json.dumps(dict(email=user_email, password=user_password)),
        headers={'Content-Type': 'application/json'}

    )
    assert code == response.status_code

@pytest.mark.parametrize(('verification_token', 'code'), (
    ('123', 204),
    ('1', 401),
    (None, 400)
))
def test_verify_email(client, auth, app, verification_token, code):
    register_result = json.loads(auth.register().data)

    with app.app_context():
        get_db().execute(
            """UPDATE user
            SET verification_token = '123', verified = 0
            WHERE access_token = ?""",
            (register_result['access_token'],)
        )

        if not verification_token:
            json_data = ''
        else:
            json_data = json.dumps(
                dict(verification_token = verification_token)
            )

        verify_response = client.post(
            '/auth/verify_email',
            data = json_data,
            headers = {
                'Content-Type': 'application/json'
            }
        )
        assert verify_response.status_code == code

@pytest.mark.parametrize(('old_password', 'new_password', 'code'), (
    ('test123456', 'test1234599', 200),
    ('test123456', 'test', 400),
    ('test1211156', 'test123123123', 401),
    (None, None, 400)
))
def test_change_password(client, auth, app, old_password, new_password, code):
    register_result = json.loads(auth.register().data)

    with app.app_context():
        if not old_password or not new_password:
            json_data = ''
        else:
            json_data = json.dumps(
                dict(
                    old_password = old_password,
                    new_password = new_password
                )
            )

        change_response = client.post(
            '/auth/change_password',
            data = json_data,
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + register_result['access_token']
            }
        )
        assert change_response.status_code == code
        if code == 200:
            assert b'access_token' in change_response.data


@pytest.mark.parametrize(('new_email', 'code'), (
    ('test2@hepitrack.com', 200),
    ('test@hepitrack.com', 409),
    ('test', 400),
    (None, 400)
))
def test_change_email(client, auth, app, new_email, code):
    register_result = json.loads(auth.register().data)

    with app.app_context():
        if not new_email:
            json_data = ''
        else:
            json_data = json.dumps(
                dict(
                    new_email = new_email
                )
            )

        change_response = client.post(
            '/auth/change_email',
            data = json_data,
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + register_result['access_token']
            }
        )
        assert change_response.status_code == code
        if code == 200:
            assert b'access_token' in change_response.data

@pytest.mark.parametrize(('verified', 'code'), (
    (0, 204),
    (1, 400)
))
def test_change_email(client, auth, app, verified, code):
    register_result = json.loads(auth.register().data)

    with app.app_context():
        get_db().execute(
            """UPDATE user
            SET verified = ?
            WHERE access_token = ?""",
            (verified, register_result['access_token'])
        )

        resend_response = client.get(
            '/auth/resend_verification',
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + register_result['access_token']
            }
        )
        assert resend_response.status_code == code

@pytest.mark.parametrize(('path', 'request_type'), (
    ('/auth/change_password', 'POST'),
    ('/auth/change_email', 'POST'),
    ('/auth/resend_verification', 'GET'),
    ('/user/data', 'GET')
))
def test_login_required(client, path, request_type):
    if request_type == 'POST':
        response = client.post(path)
    else:
        response = client.get(path)

    assert response.status_code == 401

@pytest.mark.parametrize(('path', 'request_type'), (
    ('/news/list', 'GET'),
))
def test_generic_login_required(client, path, request_type):
    if request_type == 'POST':
        response = client.post(path)
    else:
        response = client.get(path)

    assert response.status_code == 401