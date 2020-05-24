import functools, time, re

from flask import Blueprint, g

from flaskr.auth import login_required
from flaskr.db_manager import user_data

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/data', methods=['GET'])
@login_required
def data():
  return user_data(g.user['id'])