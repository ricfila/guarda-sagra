from flask import Blueprint, request, jsonify
from .connection import get_connection, jason_cur, single_jason_cur, exists_element

bp = Blueprint('tipologie', __name__)


@bp.get('/tipologie')
def get_tipologie():
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM tipologie ORDER BY posizione;")
    return jason_cur(cur)


@bp.get('/tipologie/<int:id_tipologia>')
def get_tipologia(id_tipologia):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM tipologie where id = %s;", (id_tipologia,))
    return single_jason_cur(cur)


@bp.post('/tipologie')
def create_tipologia():
    cur = get_connection().cursor()
    content = request.get_json()

    try:
        cur.execute("INSERT INTO tipologie (nome, posizione, sfondo, visibile) VALUES (%s, %s, %s, %s) RETURNING id;",
                    (content['nome'], content['posizione'], content['sfondo'], content['visibile']))
        id_tipologia = cur.fetchone()[0]
        return get_tipologia(id_tipologia), 201
    except Exception as e:
        print(e)
        return "Errore durante la creazione della tipologia", 500


@bp.put('/tipologie/<int:id_tipologia>/nome')
def update_nome_tipologia(id_tipologia):
    return update_tipologia(id_tipologia, 'nome', request.get_json()['nome'])

@bp.put('/tipologie/<int:id_tipologia>/posizione')
def update_posizione_tipologia(id_tipologia):
    return update_tipologia(id_tipologia, 'posizione', request.get_json()['posizione'])

@bp.put('/tipologie/<int:id_tipologia>/sfondo')
def update_posizione_tipologia(id_tipologia):
    return update_tipologia(id_tipologia, 'sfondo', request.get_json()['sfondo'])

@bp.put('/tipologie/<int:id_tipologia>/visibile')
def update_posizione_tipologia(id_tipologia):
    return update_tipologia(id_tipologia, 'visibile', request.get_json()['visibile'])

def update_tipologia(id_tipologia, col, value):
    cur = get_connection().cursor()
    exists, tipologia = exists_element('tipologie', id_tipologia)
    if not exists:
        return "Tipologia non trovata", 404

    try:
        cur.execute("UPDATE tipologie SET {} = %s WHERE id = %s".format(col), (id_tipologia, value))
        return get_tipologia(id_tipologia)
    except Exception as e:
        print(e)
        return "Errore durante l'aggiornamento della tipologia", 500


@bp.delete('/tipologie/<int:id_tipologia>')
def delete_tipologia(id_tipologia):
    exists, tipologia = exists_element('tipologie', id_tipologia)
    if not exists:
        return "Tipologia non trovata", 404

    cur = get_connection().cursor()
    try:
        cur.execute("DELETE FROM tipologie WHERE id = %s", (id_tipologia,))
        return jsonify(tipologia)
    except Exception as e:
        print(e)
        return "Errore durante la cancellazione della tipologia", 500
