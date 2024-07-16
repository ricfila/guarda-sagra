from flask import Blueprint, request, jsonify
from src.api.connection import get_connection, jason_cur, single_jason_cur, exists_element

bp = Blueprint('profili', __name__)


@bp.get('/profili')
def get_profili():
    cur = get_connection().cursor()
    try:
        cur.execute("SELECT * FROM profili ORDER BY nome;")
        return jason_cur(cur)
    except Exception as err:
        print(err)
        return "Errore", 500


@bp.get('/profili/<int:id_profilo>')
def get_profilo(id_profilo):
    exists, profilo = exists_element('profili', id_profilo)
    return jsonify(profilo) if exists else "Profilo non trovato", 404


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
        return single_jason_cur(cur), 201
    except Exception as err:
        print(err)
        return "Errore nell'inserimento del profilo", 500


@bp.put('/profili/<int:id_profilo>')
def update_profilo(id_profilo):
    exists, profilo = exists_element('profili', id_profilo)
    if not exists:
        return "Profilo non trovato", 404

    content = request.json
    cur = get_connection().cursor()
    try:
        cur.execute("UPDATE profili SET nome = %s, privilegi = %s, area = %s, password = %s, arrotonda = %s WHERE id = %s;",
                    (content['nome'], content['privilegi'], content['area'], content['password'], content['arrotonda'],
                     id_profilo))
        get_connection().commit()

        cur.execute("SELECT * FROM profili WHERE id = %s;", (id_profilo,))
        return single_jason_cur(cur)
    except Exception as err:
        print(err)
        return "Errore durante l'aggiornamento del profilo", 500


@bp.delete("/profili/<int:id_profilo>")
def delete_profilo(id_profilo):
    exists, profilo = exists_element('profili', id_profilo)
    if not exists:
        return "Profilo non trovato", 404

    cur = get_connection().cursor()
    try:
        # Controllo se è l'unico utente amministratore
        if profilo['privilegi'] == 1:
            cur.execute("SELECT * FROM profili WHERE privilegi = 1 AND id <> %s;", (id_profilo,))
            if cur.rowcount == 0:
                return "Impossibile cancellare il profilo amministratore, dev'essere sempre presente almeno un profilo con privilegi amministrativi", 403

        # Controllo se ci sono ordini ad esso collegati
        cur.execute("SELECT * FROM ordini WHERE cassa = %s;", (id_profilo,))
        if cur.rowcount > 0:
            return "Impossibile cancellare il profilo, ci sono {} ordini collegati ad esso".format(cur.rowcount), 403

        cur.execute("DELETE FROM profili WHERE id = %s", (id_profilo,))
        return jsonify(profilo)
    except Exception as e:
        print(e)
        return "Errore durante la cancellazione del profilo", 500
