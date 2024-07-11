from flask import Blueprint, current_app, jsonify
from src.api.connection import get_connection

bp = Blueprint('profili', __name__)


@bp.get('/profili')
def get_profili():
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM profili;")
    return jsonify(cur.fetchall())


@bp.get('/profili/<int:profili_id>')
def get_profilo(profili_id):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM profili WHERE id = {};".format(profili_id))
    return jsonify(cur.fetch())
