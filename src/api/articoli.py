from flask import Blueprint, request
from .connection import get_connection, jason_cur, single_jason_cur, col_names, jason, single_jason

bp = Blueprint('articoli', __name__)


@bp.get('/articoli')
def get_articoli():
    cur = get_connection().cursor()
    query = "SELECT * FROM articoli;"
    cur.execute(query)
    return jason_cur(cur)


@bp.get('/articoli/<int:id_articolo>')
def get_articolo(id_articolo):
    cur = get_connection().cursor()
    query = "SELECT * FROM articoli WHERE id = %s;"
    cur.execute(query, (id_articolo,))
    if cur.rowcount == 1:
        return single_jason_cur(cur)
    else:
        return "Articolo non trovato", 404


# Restituisce la lista di articoli associati al listino, ordinati secondo il campo "posizione" in articoli_listini
# La tipologia viene fornita tramite id
@bp.get('/articoli_listino/<int:listino>')
def get_articoli_listino(listino):
    cur = get_connection().cursor()
    query = """
        SELECT articoli.id, articoli.nome, articoli.nome_breve, articoli.prezzo, articoli_listini.sfondo, articoli_listini.tipologia, 
        FROM articoli_listini
        JOIN articoli ON articoli_listini.articolo = articoli.id
        JOIN tipologie ON articoli_listini.tipologia = tipologie.id
        WHERE articoli_listini.listino = %s AND articoli_listini.visibile AND tipologie.visibile
        ORDER BY articoli_listini.posizione;
    """
    cur.execute(query, (listino,))
    return jason_cur(cur)


# Restituisce la lista di articoli associati al listino, ordinati secondo l'ordine delle tipologie a cui appartengono e,
# all'interno delle singole tipologie, secondo il campo "posizione" in articoli_listini
# Vengono fornite anche le informazioni sulle tipologie: id, nome e sfondo
@bp.get('/articoli_listino_tipologie/<int:listino>')
def get_articoli_listino_tipologie(listino):
    cur = get_connection().cursor()
    query = """
        SELECT articoli.id, articoli.nome, articoli.nome_breve, articoli.prezzo, articoli_listini.sfondo, articoli_listini.tipologia, tipologie.nome as nome_tipologia, tipologie.sfondo as sfondo_tipologia
        FROM articoli_listini
        JOIN articoli ON articoli_listini.articolo = articoli.id
        JOIN tipologie ON articoli_listini.tipologia = tipologie.id
        WHERE articoli_listini.listino = %s AND articoli_listini.visibile AND tipologie.visibile
        ORDER BY tipologie.posizione, articoli_listini.posizione;
    """
    cur.execute(query, (listino,))
    return jason_cur(cur)


@bp.post('/articoli')
def create_articolo():
    content = request.get_json()
    cur = get_connection().cursor()
    query = "INSERT INTO articoli (nome, nome_breve, prezzo, copia_cliente, copia_cucina, copia_bar, copia_pizzeria, copia_rosticceria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"
    try:
        cur.execute(query, (content['nome'], content['nome_breve'], content['prezzo'],
                            content['copia_cliente'], content['copia_cucina'], content['copia_bar'],
                            content['copia_pizzeria'], content['copia_rosticceria']))
        id_articolo = cur.fetchone()[0]
        return get_articolo(id_articolo), 201
    except Exception as e:
        print(e)
        return "Errore durante l'inserimento dell'articolo", 500



@bp.put('/articoli/<int:id_articolo>')
def update_articolo(id_articolo):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM articoli WHERE id = %s;", (id_articolo,))
    if cur.rowcount == 0:
        return "Articolo non trovato", 404

    content = request.get_json()
    query = "UPDATE articoli SET nome = %s, nome_breve = %s, prezzo = %s, copia_cliente = %s, copia_cucina = %s, copia_bar = %s, copia_pizzeria = %s, copia_rosticceria = %s WHERE id = %s;"
    try:
        cur.execute(query, (content['nome'], content['nome_breve'], content['prezzo'],
                            content['copia_cliente'], content['copia_cucina'], content['copia_bar'],
                            content['copia_pizzeria'], content['copia_rosticceria'],
                            id_articolo))
        return get_articolo(id_articolo)
    except Exception as e:
        print(e)
        return "Errore durante l'aggiornamento dell'articolo", 500


@bp.delete('articoli/<int:id_articolo>')
def delete_articolo(id_articolo):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM articoli WHERE id = %s;", (id_articolo,))
    if cur.rowcount == 0:
        return "Articolo non trovato", 404

    try:
        articolo = cur.fetchone()
        cols = col_names(cur)
        cur.execute("DELETE FROM articoli WHERE id = %s;", (id_articolo,))
        return single_jason(cols, articolo)
    except Exception as e:
        print(e)
        return "Errore durante la cancellazione dell'articolo", 500
