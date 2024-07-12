from flask import Blueprint, request, jsonify
from src.api.connection import get_connection, jason, single_jason

bp = Blueprint('profili', __name__)


@bp.get('/profili')
def get_profili():
    cur = get_connection().cursor()
    try:
        cur.execute("SELECT * FROM profili;")
        return jason(cur)
    except Exception as err:
        print(err)
        return "Errore", 500


@bp.get('/profili/<int:profili_id>')
def get_profilo(profili_id):
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM profili WHERE id = {};".format(profili_id))
    return single_jason(cur)


@bp.post('/profili')
def crea_profilo():
    cur = get_connection().cursor()
    content = request.json

    try:
        cur.execute("""INSERT INTO profili (nome, privilegi, area, password, arrotonda)
                    VALUES ('{nome}', {privilegi}, {area}, '{password}', {arrotonda});"""
                    .format(nome=content['nome'],
                            privilegi=content['privilegi'],
                            area=content['area'],
                            password=content['password'],
                            arrotonda=content['arrotonda']))
        cur.execute("SELECT * FROM profili WHERE id = {};".format(cur.lastrowid))
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
        cur.execute("""UPDATE profili
                    SET nome = '{nome}', privilegi = {privilegi}, area = {area}, password = '{password}', arrotonda = '{arrotonda}'
                    WHERE id = {id};"""
                    .format(nome=content['nome'],
                            privilegi=content['privilegi'],
                            area=content['area'],
                            password=content['password'],
                            arrotonda=content['arrotonda'],
                            id=profili_id))
        cur.execute("SELECT * FROM profili WHERE id = {};".format(profili_id))
        return single_jason(cur)
    except Exception as err:
        print(err)
        return "Errore durante l'aggiornamento del profilo", 500

