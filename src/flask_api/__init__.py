from flask import Flask
app = Flask(__name__)

from . import todos

def demone():
    app.run("localhost", port=5000, debug=False)
