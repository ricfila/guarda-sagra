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
    cur.execute("SELECT * FROM ordini WHERE id = {};".format(id_ordine))
    return single_jason(cur)


@bp.post('/ordini')
def crea_ordine():
    cur = get_connection().cursor()
    content = request.json
    cur.execute("BEGIN;")

    # Inserimento ordine
    cur.execute("""INSERT INTO ordini (progressivo, data, ora, cliente, coperti, tavolo, totale, note, cassa, tipo_pagamento, menu_omaggio, per_operatori, preordine)"
                "VALUES (null, CURRENT_DATE, CURRENT_TIME, '{cliente}', {coperti}, '{tavolo}', 0, '{note}', {cassa}, {tipo_pagamento}, {menu_omaggio}, {per_operatori}, {preordine});"""
                .format(cliente=content['nome_cliente'],
                        coperti=(None if content['asporto'] else content['coperti']),
                        tavolo=content['tavolo'],
                        note=content['note_ordine'],
                        cassa=content['id_profilo'],
                        tipo_pagamento=None,
                        menu_omaggio=content['omaggio'],
                        per_operatori=content['servizio'],
                        preordine=False))
    id = cur.lastrowid

    # Inserimento articoli collegati
    totale = 0
    for a in content['articoli']:
        cur.execute("""INSERT INTO righe_articoli (ordine, articolo, quantita, note)
                    VALUES ({ordine}, {articolo}, {quantita}, '{note}');"""
                    .format(ordine=id,
                            articolo=a['id_articolo'],
                            quantita=a['qta'],
                            note=a['note']))
        cur.execute("SELECT * FROM articoli WHERE id = {};".format(a['id_articolo']))
        totale += a['qta'] * cur.fetchone()['prezzo']

    # Aggiornamento del totale
    cur.execute("""SELECT COALESCE(aree.coperto, 0) as coperto, COALESCE(aree.asporto, 0) as asporto
                FROM profili JOIN aree ON profili.area = aree.id WHERE profili.id = {};""".format(content['id_profilo']))
    info_cassa = cur.fetchone()
    totale += info_cassa['asporto'] if content['asporto'] else info_cassa['coperto'] * content['coperti']
    cur.execute("UPDATE ordini SET totale = {} WHERE id = {};".format(totale, id))

    cur.execute("COMMIT;")
    return jsonify({"id": id})
