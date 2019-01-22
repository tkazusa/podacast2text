# -*- encoding: UTF-8 -*-
from flask import Flask, jsonify
from google.cloud import storage


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    client = storage.Client()
    bucket_exists = str(client.get_bucket("mlops-215604.appspot.com").exists())

    @app.route('/')
    def index():
        return jsonify({
            "bucket exists?": bucket_exists
        })

    return app
