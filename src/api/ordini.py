from flask import Blueprint, request, jsonify
from .connection import get_connection, jason, single_jason

bp = Blueprint('ordini', __name__)


@bp.get('/ordini')
def get_ordini():
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM ordini;")
    return jason(cur)


@bp.get('/ordini/<int:id_ordine>')
def get_ordine(id_ordine):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM ordini WHERE id = %s;", (id_ordine, ))
    return single_jason(cur)


# TODO: Verificare che il commit avvenga anche su sqlite, altrimenti bisogna usare get_connection.commit()
@bp.post('/ordini')
def crea_ordine():
    cur = get_connection().cursor()
    content = request.json
    print(content)
    cur.execute("BEGIN;")

    try:
        # Inserimento ordine
        res = cur.execute(
            "INSERT INTO ordini (progressivo, data, ora, cliente, coperti, tavolo, totale, note, cassa, tipo_pagamento, menu_omaggio, per_operatori, preordine) VALUES (%s, CURRENT_DATE, CURRENT_TIME, %s, %s, %s, 0, %s, %s, %s, %s, %s, %s) RETURNING id;",
            (None, content['nome_cliente'],
             (None if content['asporto'] else (content['coperti'] if content['coperti'] != '' else 0)),
             content['tavolo'], content['note_ordine'], content['id_profilo'], 1, content['omaggio'],
             content['servizio'], False))
        id_ordine = cur.fetchone()[0]

        # Inserimento articoli collegati
        totale = 0
        for a in content['articoli']:
            cur.execute("INSERT INTO righe_articoli (ordine, articolo, quantita, note) VALUES (%s, %s, %s, %s);",
                        (id_ordine, int(a['id_articolo']), int(a['qta']), a['note']))
            cur.execute("SELECT prezzo FROM articoli WHERE id = %s;", (a['id_articolo'],))
            totale += int(a['qta']) * cur.fetchone()[0]

        # Aggiornamento del totale
        cur.execute(
            "SELECT COALESCE(aree.coperto, 0) as coperto, COALESCE(aree.asporto, 0) as asporto FROM profili JOIN aree ON profili.area = aree.id WHERE profili.id = %s;",
            (content['id_profilo'],))
        if cur.rownumber > 0:  # Solo se la cassa è associata a un'area, altrimenti non ha costi del servizio
            info_cassa = cur.fetchone()
            totale += (info_cassa[1] if content['asporto'] else info_cassa[0]) * content['coperti']
        cur.execute("UPDATE ordini SET totale = %s WHERE id = %s;", (totale, id_ordine))

        cur.execute("COMMIT;")

        cur.execute("SELECT * FROM ordini WHERE id = %s;", (id_ordine,))
        return single_jason(cur)
    except Exception as e:
        print(e)
        cur.execute("ROLLBACK;")
        return "Errore durante la creazione dell'ordine", 500
