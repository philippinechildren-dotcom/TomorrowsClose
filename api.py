from flask import Flask, jsonify

from Utilities.Publishing.publisher import (
    build_homepage,
    build_free,
    build_paid,
)

app = Flask(__name__)


@app.route("/json/homepage")
def homepage_json():
    return jsonify(build_homepage())


@app.route("/json/free")
def free_json():
    return jsonify(build_free())


@app.route("/json/paid")
def paid_json():
    return jsonify(build_paid())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)