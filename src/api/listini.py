from flask import Blueprint, jsonify
from .connection import get_connection, jason, single_jason

bp = Blueprint('listini', __name__)


@bp.get('/listini_cassa/<int:cassa>')
def get_listini_cassa(cassa):
    cur = get_connection().cursor()
    query = """
        SELECT listini.id, listini.nome
        FROM casse_listini JOIN listini ON casse_listini.listino = listini.id
        WHERE casse_listini.cassa = %s AND
        (casse_listini.data_inizio <= CURRENT_DATE OR casse_listini.data_inizio IS NULL) AND
        (casse_listini.data_fine >= CURRENT_DATE OR casse_listini.data_fine IS NULL);
    """
    cur.execute(query, (cassa,))
    return jason(cur)
