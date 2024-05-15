import sqlite3
import psycopg2
import threading
from config import config
import os

# Usa un oggetto threading.local per mantenere una connessione per ogni thread
_thread_locals = threading.local()

def get_connection():
    # Se non c'è una connessione associata a questo thread, creane una
    if not hasattr(_thread_locals, 'connection'):
        if config['SQLite']['enabled'] == "true" or config['SQLite']['enabled'] == "True":
            _thread_locals.connection = sqlite3.connect("dblite.db")
        else:
            _thread_locals.connection = psycopg2.connect(database=config['PostgreSQL']['database'],
                                    host=config['PostgreSQL']['server'],
                                    user=config['PostgreSQL']['username'],
                                    password=config['PostgreSQL']['password'],
                                    port=config['PostgreSQL']['port'])
    return _thread_locals.connection


def create_connection():
    cur = get_connection().cursor()
    path_to_sqlite_db = os.path.join(os.getcwd(), "guarda-sagra-sqlite.sql")
    path_to_postgres_db = os.path.join(os.getcwd(), "guarda-sagra-postgres.sql")
    # Eventuale creazione delle tabelle
    if config['SQLite']['enabled'] == "true":
        with open(path_to_sqlite_db) as f:
            cur.executescript(f.read())
    else:
        with open(path_to_postgres_db) as f:
            cur.execute(f.read())

    # Se non è presente un utente admin ne crea uno, con nome admin e password admin
    cur.execute("SELECT COUNT(*) FROM profili WHERE privilegi = 1;")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO profili (nome, privilegi, password) VALUES ('admin', 1, 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec');")
        get_connection().commit()

    return get_connection(), cur
