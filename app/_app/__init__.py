# -*- encoding: UTF-8 -*-
from flask import Flask
from google.cloud import storage

from .views import transcriber


def create_app() -> type(Flask):
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.register_blueprint(transcriber)

    client = storage.Client()

    return app
