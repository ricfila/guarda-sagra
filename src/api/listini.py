from flask import Blueprint, jsonify, request
from .connection import get_connection, jason_cur, exists_element

bp = Blueprint('listini', __name__)


@bp.get('/listini')
def get_listini():
    cur = get_connection().cursor()
    query = """
        SELECT *
        FROM listini
        ORDER BY nome;
        """
    cur.execute(query, )
    return jason_cur(cur)

@bp.get('/listini/<int:id_listino>')
def get_listino(id_listino):
    exists, listino = exists_element('listini', id_listino)
    return jsonify(listino) if exists else "Listino non trovato", 404


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
    return jason_cur(cur)


@bp.post('/listini')
def create_listino():
    content = request.get_json()
    cur = get_connection().cursor()
    query = "INSERT INTO listini (nome) VALUES (%s) RETURNING id;"
    try:
        cur.execute(query, (content['nome'],))
        id_listino = cur.fetchone()[0]
        return get_listino(id_listino), 201
    except Exception as e:
        print(e)
        return "Errore durante la creazione del listino", 500


@bp.put('/listini/<int:id_listino>')
def update_listino(id_listino):
    exists, listino = exists_element('listini', id_listino)
    if not exists:
        return "Listino non trovato", 404

    cur = get_connection().cursor()
    content = request.get_json()
    query = "UPDATE listini SET nome = %s WHERE id = %s;"
    try:
        cur.execute(query, (content['nome'], id_listino))
        return get_listino(id_listino)
    except Exception as e:
        print(e)
        return "Errore durante l'aggiornamento del listino", 500


@bp.delete('/listini/<int:id_listino>')
def delete_listino(id_listino):
    exists, listino = exists_element('listini', id_listino)
    if not exists:
        return "Listino non trovato", 404

    cur = get_connection().cursor()
    try:
        cur.execute("DELETE FROM listini WHERE id = %s;", (id_listino,))
        return jsonify(listino)
    except Exception as e:
        print(e)
        return "Errore durante la cancellazione del listino", 500
