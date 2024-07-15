from flask import Blueprint, request
from src.api.connection import get_connection, jason_cur, single_jason_cur, col_names, jason, single_jason

bp = Blueprint('aree', __name__)


@bp.get('/aree')
def get_aree():
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM aree ORDER BY nome;")
    return jason_cur(cur)


@bp.get('/aree/<int:aree_id>')
def get_area(aree_id):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM aree WHERE id = %s;", (aree_id,))
    return single_jason_cur(cur)


@bp.post('/aree')
def create_area():
    content = request.get_json()
    cur = get_connection().cursor()
    query = "INSERT INTO aree (nome, coperto, asporto) VALUES (%s, %s, %s); RETURNING id;"
    try:
        cur.execute(query, (content['nome'], content['coperto'], content['asporto']))
        id_area = cur.fetchone()[0]
        return get_area(id_area), 201
    except Exception as e:
        print(e)
        return "Errore durante la creazione dell'area", 500


@bp.put('/aree/<int:id_area>')
def update_area(id_area):
    cur = get_connection().cursor()
    query = "INSERT INTO aree (nome, coperto, asporto) VALUES (%s, %s, %s); RETURNING id;"
    content = request.get_json()
    try:
        cur.execute(query, (content['nome'], content['coperto'], content['asporto']))
        id_area = cur.fetchone()[0]
        return get_area(id_area)
    except Exception as e:
        print(e)
        return "Errore durante la creazione dell'area", 500


@bp.delete('/aree/<int:id_area>')
def delete_area(id_area):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM aree WHERE id = %s;", (id_area,))
    if cur.rowcount == 0:
        return "Area non trovata", 404

    try:
        area = cur.fetchone()
        cols = col_names(cur)
        cur.execute("DELETE FROM aree WHERE id = %s;", (id_area,))
        return single_jason(cols, area)
    except Exception as e:
        print(e)
        return "Errore durante la cancezione dell'area", 500

