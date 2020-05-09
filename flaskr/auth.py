import functools
import time
import re

from flask import (
    Blueprint, flash, g, request, session, abort, jsonify, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from passlib.hash import sha256_crypt

from flaskr.db_manager import (
        get_user_by_email, get_user_by_token, insert_user, update_user_token
)

from marshmallow import Schema, fields, ValidationError, validate

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    content=request.get_json()
    if not content:
        abort(400)
    try:
        email = content['email']
        password = content['password']

        UserSchema().load(
            {'email': email, 'password': password}
        )
    except KeyError:
        abort(400)
    except ValidationError as validation_error:
        abort(400, validation_error.messages)

    if (
            email is not None
            and password is not None
            and get_user_by_email(email) is None
        ):
        token = sha256_crypt.hash(email + password + str(time.time_ns()))
        insert_user(email, generate_password_hash(password), token)
        
        return jsonify(access_token=token)
    else:
        abort(409)

@bp.route('/login', methods=['POST'])
def login():
    content=request.get_json()
    if not content:
        abort(400)
    try:
        email = content['email']
        password = content['password']

        UserSchema().load(
            {'email': email, 'password': password}
        )
    except KeyError:
        abort(400)
    except ValidationError as validation_error:
        abort(400, validation_error.messages)

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user['password'], password):
        abort(401)
    else:
        token = sha256_crypt.hash(email + password + str(time.time_ns()))
        update_user_token(token, user['id'])
        return jsonify(access_token=token)

@bp.before_app_request
def load_logged_in_user():
    auth_header = request.headers.get('Authorization')
    user_token = read_authorization_header(auth_header)

    g.user = None
    g.generic_request = False
    
    if user_token is not None:
        g.user = get_user_by_token(user_token)
        if user_token == current_app.config['API_KEY']:
            g.generic_request = True

def read_authorization_header(auth_header):
    user_token = None

    if auth_header:
        split_header = auth_header.split(' ')
        if len(split_header) > 1:
            user_token = split_header[1]
            
    return user_token

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            abort(401)
        return view(**kwargs)
    return wrapped_view

def generic_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.generic_request != True:
            abort(401)
        return view(**kwargs)
    return wrapped_view

class UserSchema(Schema):
    email = fields.Email()
    password = fields.Str(validate=validate.Length(min=6))
