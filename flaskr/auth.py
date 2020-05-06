from flask import Flask, Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('login', methods=['POST'])
def login():
    return 'a'
