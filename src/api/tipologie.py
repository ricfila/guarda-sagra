from flask import Blueprint
from .connection import get_connection, jason, single_jason

bp = Blueprint('tipologie', __name__)


@bp.get('/tipologie')
def get_tipologie():
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM tipologie ORDER BY posizione;")
    return jason(cur)


@bp.get('/tipologie/<int:tipologie_id>')
def get_tipologia(tipologie_id):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM tipologie where id = %s;", (tipologie_id,))
    return single_jason(cur)

