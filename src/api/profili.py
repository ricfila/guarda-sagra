from flask import Blueprint, request, jsonify
from src.api.connection import get_connection, jason, single_jason

bp = Blueprint('profili', __name__)


@bp.get('/profili')
def get_profili():
    cur = get_connection().cursor()
    try:
        cur.execute("SELECT * FROM profili ORDER BY nome;")
        return jason(cur)
    except Exception as err:
        print(err)
        return "Errore", 500


@bp.get('/profili/<int:profili_id>')
def get_profilo(profili_id):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM profili WHERE id = %s;", (profili_id,))
    if cur.rowcount == 1:
        return single_jason(cur)
    else:
        return "Profilo non trovato", 404


@bp.post('/profili')
def crea_profilo():
    cur = get_connection().cursor()
    content = request.json
    try:
        cur.execute("INSERT INTO profili (nome, privilegi, area, password, arrotonda) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                    (content['nome'], content['privilegi'], content['area'], content['password'], content['arrotonda']))
        get_connection().commit()

        id_profilo = cur.fetchone()[0]
        cur.execute("SELECT * FROM profili WHERE id = %s;", (id_profilo,))
        return single_jason(cur)
    except Exception as err:
        print(err)
        return "Errore nell'inserimento del profilo", 500


@bp.put('/profili/<int:profili_id>')
def update_profilo(profili_id):
    content = request.json
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM profili WHERE id = {};".format(profili_id))
    if cur.rowcount == 0:
        return "Profilo non trovato", 404
    try:
        cur.execute("UPDATE profili SET nome = %s, privilegi = %s, area = %s, password = %s, arrotonda = %s WHERE id = %s;",
                    (content['nome'], content['privilegi'], content['area'], content['password'], content['arrotonda'],
                     profili_id))
        get_connection().commit()

        cur.execute("SELECT * FROM profili WHERE id = %s;", (profili_id,))
        return single_jason(cur)
    except Exception as err:
        print(err)
        return "Errore durante l'aggiornamento del profilo", 500

