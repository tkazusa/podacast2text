# -*- coding: UTF-8 -*-
from flask import Flask
from google.cloud import storage

from .views.index import transcriber


UPLOAD_FOLDER = '/path/to/the/uploads'


def create_app() -> type(Flask):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['JSON_AS_ASCII'] = False
    app.register_blueprint(transcriber)
    client = storage.Client()

    return app
