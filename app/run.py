# -*- encoding: UTF-8 -*-
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII']


@app.route('/')
def index():
    return jsonify({
        "message": "テスト!!"
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
