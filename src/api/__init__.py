from flask import Flask
from .connection import create_connection, get_connection


def create_app():
    app = Flask(__name__)

    # Connessione al database
    create_connection()

    # Importa le route dagli altri file
    from . import profiles

    # Registra le route
    app.register_blueprint(profiles.bp)

    return app


def init_thread():
    app = create_app()
    app.run("localhost", port=5000, debug=False)
