import functools, time, re

from flask import Blueprint, g, request, abort

from flaskr.auth import login_required
from flaskr.db_manager import user_data, update_color
from marshmallow import Schema, fields, ValidationError, validate

bp=Blueprint('user', __name__, url_prefix='/user')

@bp.route('/data', methods=['GET'])
@login_required
def data():
    return user_data(g.user['id'])

@bp.route('/color', methods=['PATCH'])
@login_required
def patch_color():
    content=request.get_json()
    if not content:
        abort(400)
    try:
        color=content['color']

        ColorSchema().load(
            {'color': color}
        )
    except ValidationError as validation_error:
        abort(400, validation_error.messages)
    except:
        abort(400)

    update_color(color)

    return ('', 204)

class ColorSchema(Schema):
    color=fields.Str(
        required=True,
        validate=validate.Regexp('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    )