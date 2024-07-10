from flask import Blueprint, current_app, jsonify
from .connection import get_connection

bp = Blueprint('tipologie', __name__)


@bp.get('/tipologie')
def get_tipologie():
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM tipologie")
    return jsonify(cur.fetchall())


@bp.get('/tipologie/<int:tipologie_id>')
def get_tipologia(tipologie_id):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM tipologie where id = {};".format(tipologie_id))
    return jsonify(cur.fetch())

