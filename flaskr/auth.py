import functools

import time

from flask import (
    Blueprint, flash, g, request, session, abort, jsonify
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from passlib.hash import sha256_crypt

import re

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    content=request.get_json()
    try:
        email = content['email']
        password = content['password']
    except (KeyError):
        abort(400)
    db = get_db()

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        abort(400, 'Wrong email format')


    if email is not None and password is not None and db.execute(
            'SELECT id FROM user WHERE email = ?',
            (email,)
        ).fetchone() is None:

        token = sha256_crypt.hash(email + password + str(time.time_ns()))

        db.execute(
            'INSERT INTO user (email, password, access_token) VALUES (?, ?, ?)',
            (email, generate_password_hash(password), token)
        )
        db.commit()
        return jsonify(access_token=token)
    else:
        abort(409)

@bp.route('/login', methods=['POST'])
def login():
    content=request.get_json()
    try:
        email = content['email']
        password = content['password']
    except (KeyError):
        abort(400)
    db = get_db()

    user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

    if user is None or not check_password_hash(user['password'], password):
        abort(401)
    else:
        token = sha256_crypt.hash(email + password + str(time.time_ns()))
        db.execute('UPDATE user SET access_token = ?', (token,))
        db.commit()
        return jsonify(access_token=token)

@bp.before_app_request
def load_logged_in_user():
    user_token = request.headers.get('Authorization')
    if user_token is None:
        g.user = None
    else:
        g.user = get_db().execute(
                'SELECT * FROM user WHERE access_token = ?', (user_token,)
                ).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            abort(401)

        return view(**kwargs)

    return wrapped_view
