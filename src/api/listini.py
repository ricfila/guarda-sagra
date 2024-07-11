from flask import Blueprint, current_app, jsonify
from .connection import get_connection

bp = Blueprint('listini', __name__)


@bp.get('/listini_cassa/<int:cassa>')
def get_listini_cassa(cassa):
    cur = get_connection().cursor()
    cur.execute("""SELECT listini.id, listini.nome
                FROM casse_listini JOIN listini ON casse_listini.listino = listini.id
                WHERE casse_listini.cassa = {} AND
                (casse_listini.data_inizio <= CURRENT_DATE OR casse_listini.data_inizio IS NULL) AND
                (casse_listini.data_fine >= CURRENT_DATE OR casse_listini.data_fine IS NULL);""".format(cassa))
    return jsonify(cur.fetchall())


# Restituisce la lista di articoli associati al listino, ordinati secondo il campo "posizione" in articoli_listini
@bp.get('/articoli_listino/<int:listino>')
def get_articoli_listino(listino):
    cur = get_connection().cursor()
    cur.execute("""SELECT articoli.id, articoli.nome, articoli.nome_breve, articoli.tipologia, articoli.prezzo, articoli_listini.sfondo
                FROM articoli_listini JOIN articoli ON articoli_listini.articolo = articoli.id
                WHERE articoli_listini.listini = {} AND articoli_listini.visibile
                ORDER BY articoli_listini.posizione;""".format(listino))
    return jsonify(cur.fetchall())


# Restituisce la lista di articoli associati al listino, ordinati secondo l'ordine delle tipologie a cui appartengono e,
# all'interno delle singole tipologie, secondo il campo "posizione" in articoli_listini
@bp.get('/articoli_listino_tipologie/<int:listino>')
def get_articoli_listino_tipologie(listino):
    cur = get_connection().cursor()
    cur.execute("""SELECT articoli.id, articoli.nome, articoli.nome_breve, articoli.tipologia, articoli.prezzo, articoli_listini.sfondo
                FROM articoli_listini
                JOIN articoli ON articoli_listini.articolo = articoli.id
                JOIN tipologie ON articoli.tipologia = tipologie.id
                WHERE articoli_listini.listini = {} AND articoli_listini.visibile
                ORDER BY tipologie.posizione, articoli_listini.posizione;""".format(listino))
    return jsonify(cur.fetchall())
