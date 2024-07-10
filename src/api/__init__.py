from flask import Flask
from .connection import create_connection, get_connection


def create_app():
    app = Flask(__name__)

    # Importa le route dagli altri file
    from . import profili
    from . import listini
    from . import tipologie

    # Registra le route
    app.register_blueprint(profili.bp)
    app.register_blueprint(listini.bp)
    app.register_blueprint(tipologie.bp)

    return app


def init_thread():
    app = create_app()
    create_connection()
    app.run("localhost", port=5000, debug=False)
