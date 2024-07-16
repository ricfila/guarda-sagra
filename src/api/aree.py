from flask import Blueprint, request, jsonify
from src.api.connection import get_connection, jason_cur, exists_element

bp = Blueprint('aree', __name__)


@bp.get('/aree')
def get_aree():
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM aree ORDER BY nome;")
    return jason_cur(cur)


@bp.get('/aree/<int:id_area>')
def get_area(id_area):
    exists, area = exists_element('aree', id_area)
    return jsonify(area) if exists else ("Area non trovata", 404)


@bp.post('/aree')
def create_area():
    content = request.get_json()
    cur = get_connection().cursor()
    query = "INSERT INTO aree (nome, coperto, asporto) VALUES (%s, %s, %s); RETURNING id;"
    try:
        cur.execute(query, (content['nome'], content['coperto'], content['asporto']))
        get_connection().commit()
        id_area = cur.fetchone()[0]
        return get_area(id_area), 201
    except Exception as e:
        print(e)
        return "Errore durante la creazione dell'area", 500


@bp.put('/aree/<int:id_area>')
def update_area(id_area):
    exists, area = exists_element('aree', id_area)
    if not exists:
        return "Area non trovata", 404

    cur = get_connection().cursor()
    content = request.get_json()
    query = "UPDATE aree SET nome = %s, coperto = %s, asporto = %s WHERE id = %s;"
    try:
        cur.execute(query, (content['nome'], content['coperto'], content['asporto']), id_area)
        get_connection().commit()
        return get_area(id_area)
    except Exception as e:
        print(e)
        return "Errore durante l'aggiornamento dell'area", 500


@bp.delete('/aree/<int:id_area>')
def delete_area(id_area):
    exists, area = exists_element('aree', id_area)
    if not exists:
        return "Area non trovata", 404

    cur = get_connection().cursor()
    try:
        cur.execute("DELETE FROM aree WHERE id = %s;", (id_area,))
        get_connection().commit()
        return jsonify(area)
    except Exception as e:
        print(e)
        return "Errore durante la cancezione dell'area", 500

