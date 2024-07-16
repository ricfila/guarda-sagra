from flask import Flask
from .connection import create_connection, get_connection


def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False

    # Importa le route dagli altri file
    from . import aree
    from . import articoli
    from . import listini
    from . import ordini
    from . import profili
    from . import statistiche
    from . import tipologie

    # Registra le route
    app.register_blueprint(aree.bp)
    app.register_blueprint(articoli.bp)
    app.register_blueprint(listini.bp)
    app.register_blueprint(ordini.bp)
    app.register_blueprint(profili.bp)
    app.register_blueprint(statistiche.bp)
    app.register_blueprint(tipologie.bp)

    return app


def init_thread():
    app = create_app()
    create_connection()
    app.run("localhost", port=5000, debug=False, threaded=True)
