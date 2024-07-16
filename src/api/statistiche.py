from flask import Blueprint, request, jsonify, json, Response
from src.api.connection import get_connection, jason_cur, exists_element, col_names, dict_res, single_jason_cur

bp = Blueprint('statistiche', __name__)


@bp.get('/stats/vendite')
def get_vendite():
    cur = get_connection().cursor()
    query = """
        SELECT id_articolo, nome, quantita, data
        FROM articoli JOIN (
            SELECT righe_articoli.articolo as id_articolo, sum(quantita) as quantita, ordini.data
            FROM righe_articoli
            JOIN ordini ON righe_articoli.ordine = ordini.id
            GROUP BY righe_articoli.articolo, ordini.data
            ORDER BY ordini.data
        ) as a ON articoli.id = a.id_articolo
    """
    cur.execute(query)
    articoli = []
    while (row := cur.fetchone()) is not None:
        index = next((i for i, item in enumerate(articoli) if item['id'] == row[0]), -1)
        if index == -1:
            articoli.append({'id': row[0], 'nome': row[1], 'quantita': [{'data': row[3], 'qta': row[2]}]})
        else:
            articoli[index]['quantita'].append({'data': row[3], 'qta': row[2]})

    return Response(json.dumps(articoli, default=str), mimetype='application/json')


@bp.get('/stats/vendite/<string:data>')
def get_vendite_giorno(data):
    cur = get_connection().cursor()
    query = """
        SELECT id_articolo, nome, quantita
        FROM articoli JOIN (
            SELECT righe_articoli.articolo as id_articolo, sum(quantita) as quantita
            FROM righe_articoli
            JOIN ordini ON righe_articoli.ordine = ordini.id
            WHERE data = %s
            GROUP BY righe_articoli.articolo
        ) as a ON articoli.id = a.id_articolo
    """
    cur.execute(query, (data,))
    articoli = []
    while (row := cur.fetchone()) is not None:
        articoli.append({'id': row[0], 'nome': row[1], 'quantita': row[2]})

    return jsonify(articoli)


@bp.get('/stats/servizio')
def get_servizio():
    cur = get_connection().cursor()
    query = """
        SELECT data, COALESCE(sum(coperti), 0) as coperti,
        sum(CASE WHEN coperti is null THEN 1 ELSE 0 END) as asporto, sum(totale) as totale
        FROM ordini GROUP BY data ORDER BY data;
    """
    cur.execute(query)
    cols = col_names(cur)
    servizio = [dict(zip(cols, row)) for row in cur.fetchall()]
    return Response(json.dumps(servizio, default=str), mimetype='application/json')


@bp.get('/stats/servizio/<string:data>')
def get_servizio_giorno(data):
    cur = get_connection().cursor()
    query = """
        SELECT COALESCE(sum(coperti), 0) as coperti,
        sum(CASE WHEN coperti is null THEN 1 ELSE 0 END) as asporto, sum(totale) as totale
        FROM ordini WHERE data = %s;
    """
    cur.execute(query, (data,))
    return single_jason_cur(cur)


@bp.get('/stats/incasso/<string:data>')
def get_incasso(data):
    cur = get_connection().cursor()
    query = """
        SELECT tipi_pagamento.nome as tipo_pagamento, totale
        FROM tipi_pagamento JOIN (
            SELECT ordini.tipo_pagamento as tipo_pagamento, sum(ordini.totale) as totale
            FROM ordini
            JOIN tipi_pagamento ON ordini.tipo_pagamento = tipi_pagamento.id
            WHERE data = %s
            GROUP BY ordini.tipo_pagamento
        ) as q on tipi_pagamento.id = q.tipo_pagamento ORDER BY tipi_pagamento.posizione;
    """
    cur.execute(query, (data,))
    return jason_cur(cur)


@bp.get('/stats/incasso/<string:data>/cassa/<int:cassa>')
def get_incasso_cassa(data, cassa):
    cur = get_connection().cursor()
    query = """
        SELECT tipi_pagamento.nome as tipo_pagamento, sum(ordini.totale) as totale
        FROM ordini JOIN tipi_pagamento ON ordini.tipo_pagamento = tipi_pagamento.id
        WHERE data = %s AND cassa = %s
        GROUP BY tipi_pagamento.id ORDER BY tipi_pagamento.posizione;
    """
    cur.execute(query, (data, cassa))
    return jason_cur(cur)
