from flask import Blueprint, current_app, jsonify
from .connection import get_connection

bp = Blueprint('profiles', __name__)


@bp.get('/profiles')
def index():
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM profili")
    return jsonify(cur.fetchall())