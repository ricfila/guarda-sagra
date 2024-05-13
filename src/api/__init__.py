from flask import Flask
from config import config
import sqlite3
import psycopg2

app = Flask(__name__)

from . import todos


def demone():
    db_init()
    app.run("localhost", port=5000, debug=False)


def db_init():
    # Connessione al database
    if config['SQLite']['enabled'] == "true" or config['SQLite']['enabled'] == "True":
        print("SQLite")
        conn = sqlite3.connect("../dblite.db")
    else:
        print("PostgreSQL")
        conn = psycopg2.connect(database=config['PostgreSQL']['database'],
                                host=config['PostgreSQL']['server'],
                                user=config['PostgreSQL']['username'],
                                password=config['PostgreSQL']['password'],
                                port=config['PostgreSQL']['port'])
    global cur
    cur = conn.cursor()

    # Eventuale creazione delle tabelle
    with open("../guarda-sagra-sqlite.sql" if config['SQLite']['enabled'] == "true" else "../guarda-sagra-postgres.sql") as f:
        cur.execute(f.read())

    # Se non è presente un utente admin ne crea uno, con nome admin e password admin
    cur.execute("SELECT COUNT(*) FROM profili WHERE privilegi = 1;")
    # SEPARARE SCRIPT DI CREAZIONE POSTGRES (e aggiungere autoincrement agli id) E SQLITE
    if cur.fetchone()[0] == 0:
        #cur.execute("INSERT INTO \"profili\" (\"nome\", \"privilegi\", \"password\") VALUES (\"admin\", 1, \"c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec\");")
        conn.commit()
