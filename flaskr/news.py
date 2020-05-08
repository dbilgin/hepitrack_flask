from flask import Blueprint, g

from flaskr.auth import login_required

bp = Blueprint('news', __name__, url_prefix='/news')

@bp.route('/list', methods=['GET'])
@login_required
def list():
    return 'MAA: ' + g.user['email']
