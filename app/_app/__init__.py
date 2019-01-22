# -*- encoding: UTF-8 -*-
from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False

    @app.route('/')
    def index():
        return jsonify({
            "message": "bbb"
        })

    return app
