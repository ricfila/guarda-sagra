from flask import Blueprint
from .connection import get_connection, jason, single_jason

bp = Blueprint('articoli', __name__)


# Restituisce la lista di articoli associati al listino, ordinati secondo il campo "posizione" in articoli_listini
# La tipologia viene fornita tramite id
@bp.get('/articoli_listino/<int:listino>')
def get_articoli_listino(listino):
    cur = get_connection().cursor()
    cur.execute("""SELECT articoli.id, articoli.nome, articoli.nome_breve, articoli.prezzo, articoli_listini.sfondo, articoli_listini.tipologia, 
                FROM articoli_listini
                JOIN articoli ON articoli_listini.articolo = articoli.id
                JOIN tipologie ON articoli_listini.tipologia = tipologie.id
                WHERE articoli_listini.listino = {} AND articoli_listini.visibile AND tipologie.visibile
                ORDER BY articoli_listini.posizione;""".format(listino))
    return jason(cur)


# Restituisce la lista di articoli associati al listino, ordinati secondo l'ordine delle tipologie a cui appartengono e,
# all'interno delle singole tipologie, secondo il campo "posizione" in articoli_listini
# Vengono fornite anche le informazioni sulle tipologie: id, nome e sfondo
@bp.get('/articoli_listino_tipologie/<int:listino>')
def get_articoli_listino_tipologie(listino):
    cur = get_connection().cursor()
    cur.execute("""SELECT articoli.id, articoli.nome, articoli.nome_breve, articoli.prezzo, articoli_listini.sfondo, articoli_listini.tipologia, tipologie.nome, tipologie.sfondo
                FROM articoli_listini
                JOIN articoli ON articoli_listini.articolo = articoli.id
                JOIN tipologie ON articoli_listini.tipologia = tipologie.id
                WHERE articoli_listini.listino = {} AND articoli_listini.visibile AND tipologie.visibile
                ORDER BY tipologie.posizione, articoli_listini.posizione;""".format(listino))
    return jason(cur)
