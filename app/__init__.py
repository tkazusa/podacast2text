# -*- encoding: UTF-8 -*-
from flask import Flask, jsonify


def create_app(test_config=None):
    """"Crete and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['JSON_AS_ASCII']

    @app.route('/')
    def index():
        return jsonify({
            "message": "test"
        })

    return app
