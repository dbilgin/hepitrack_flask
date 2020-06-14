import functools, time, re

from flask import (
  Blueprint, flash, g, request, session, abort, jsonify, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from passlib.hash import sha256_crypt
from marshmallow import Schema, fields, ValidationError, validate

from flaskr.db import get_db
from flaskr.db_manager import (
  get_user_by_email,
  get_user_by_token,
  insert_user,
  update_user_token,
  verify_user,
  update_user_token_and_pass,
  update_email,
  update_verification_token,
  check_user_count_by_email,
  delete_user,
  log_out_user,
  update_user_pass_by_verify_token,
  update_verification_token_by_email
)
from flaskr.email import (
    send_email,
    email_verification_data,
    email_reset_password
)
from flask_cors import cross_origin
from random import randint

bp=Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    auth_header=request.headers.get('Authorization')
    user_token=read_authorization_header(auth_header)

    g.user=None
    g.generic_request=False

    if user_token is not None:
        g.user=get_user_by_token(user_token)
        if user_token==current_app.config['API_KEY']:
            g.generic_request=True

def read_authorization_header(auth_header):
    user_token=None

    if auth_header:
        split_header=auth_header.split(' ')
        if len(split_header) > 1:
            user_token=split_header[1]

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
        if g.generic_request !=True:
            abort(401)
        return view(**kwargs)
    return wrapped_view

class UserSchema(Schema):
    email=fields.Email()
    password=fields.Str(validate=validate.Length(min=6))

@bp.route('/register', methods=['POST'])
def register():
    content=request.get_json()
    if not content:
        abort(400)
    try:
        email=content['email']
        password=content['password']

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
        token=sha256_crypt.hash(email + password + str(time.time()))
        verification_token=sha256_crypt.hash(str(time.time()))
        insert_user(
          email,
          generate_password_hash(password),
          token,
          verification_token
        )

        send_email(email, email_verification_data(verification_token))

        return jsonify(access_token=token)
    else:
        abort(409)

@bp.route('/login', methods=['POST'])
def login():
    content=request.get_json()
    if not content:
        abort(400)
    try:
        email=content['email']
        password=content['password']

        UserSchema().load(
                {'email': email, 'password': password}
        )
    except KeyError:
        abort(400)
    except ValidationError as validation_error:
        abort(400, validation_error.messages)

    user=get_user_by_email(email)
    if user is None or not check_password_hash(user['password'], password):
        abort(401)
    else:
        token=sha256_crypt.hash(email + password + str(time.time()))
        update_user_token(token, user['id'])
        return jsonify(access_token=token,verified=user['verified'])

@bp.route('/verify_email', methods=['POST'])
@cross_origin(['https://www.hepitrack.com'])
def verify_email():
    content=request.get_json()
    if not content:
        abort(400)
    try:
        verification_token=content['verification_token']
    except:
        abort(400)

    if verify_user(verification_token)==0:
      abort(401)
    else:
      return ('', 204)

@bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    content=request.get_json()
    if not content:
        abort(400)
    try:
        old_password=content['old_password']
        new_password=content['new_password']

        UserSchema().load(
                {'password': new_password}
        )
    except KeyError:
        abort(400)
    except ValidationError as validation_error:
        abort(400, validation_error.messages)

    if (
            check_password_hash(g.user['password'], old_password)
            and g.user['verified'] == 1
        ):
      token=sha256_crypt.hash(g.user['email']
        + new_password
        + str(time.time()))
      update_user_token_and_pass(token, generate_password_hash(new_password))

      return jsonify(access_token=token)
    else:
        abort(401)

@bp.route('/change_email', methods=['POST'])
@login_required
def change_email():
    content=request.get_json()
    if not content:
        abort(400)
    try:
        new_email=content['new_email']
        UserSchema().load(
            {'email': new_email}
        )
    except KeyError:
        abort(400)
    except ValidationError as validation_error:
        abort(400, validation_error.messages)

    if check_user_count_by_email(new_email) > 0:
        abort(409)

    if g.user['verified'] != 1:
        abort(401)

    token=sha256_crypt.hash(
      new_email
      + g.user['password']
      + str(time.time())
    )
    verification_token=sha256_crypt.hash(str(time.time()))
    update_email(new_email, token, verification_token)

    send_email(new_email, email_verification_data(verification_token))

    return jsonify(access_token=token)

@bp.route('/resend_verification', methods=['GET'])
@login_required
def resend_verification():
    verification_token=sha256_crypt.hash(str(time.time()))
    db_result=update_verification_token(verification_token)

    if db_result.rowcount > 0:
      send_email(g.user['email'], email_verification_data(verification_token))
    else:
      abort(400)

    return ('', 204)

@bp.route('/delete_account', methods=['DELETE'])
@login_required
def delete_account():
    try:
        delete_user()
    except:
        abort(400)

    return ('', 204)

@bp.route('/log_out', methods=['GET'])
@login_required
def log_out():
    try:
        log_out_user()
    except:
        abort(400)

    return ('', 204)

@bp.route('/reset_password_request', methods=['POST'])
def reset_password_request():
    content=request.get_json()
    if not content:
        abort(400)
    try:
        user_email=content['email']
    except:
        abort(400)

    verification_token=sha256_crypt.hash(str(time.time()))
    db_result=update_verification_token_by_email(verification_token, user_email)

    if db_result.rowcount > 0:
      send_email(user_email, email_reset_password(verification_token))
    else:
      abort(400)

    return ('', 204)

@bp.route('/reset_password', methods=['POST'])
def reset_password():
    content=request.get_json()
    if not content:
        abort(400)
    try:
        verification_token=content['verification_token']
    except:
        abort(400)

    new_password=randint(10**(6-1), (10**6)-1)
    db_result=update_user_pass_by_verify_token(new_password, verification_token)

    if db_result.rowcount > 0:
        return ('', 204)
    else:
        abort(401)