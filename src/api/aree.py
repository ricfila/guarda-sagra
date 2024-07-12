from flask import Blueprint
from src.api.connection import get_connection, jason, single_jason

bp = Blueprint('aree', __name__)


@bp.get('/aree')
def get_aree():
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM aree;")
    return jason(cur)


@bp.get('/aree/<int:aree_id>')
def get_area(aree_id):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM aree WHERE id = {};".format(aree_id))
    return single_jason(cur)
