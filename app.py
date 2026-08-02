from flask import Flask, render_template, jsonify
from catalog import render_catalog

app = Flask(__name__)


@app.route("/")
def catalog():
    return render_catalog()

@app.route("/prototype")
def prototype():
    return render_template("homepage_test.html")

@app.route("/json/homepage")
def homepage_json():

    from Utilities.Publishing.publisher import build_homepage

    return jsonify(build_homepage())

@app.route("/json/free")
def free_json():

    from Utilities.Publishing.publisher import build_free

    return jsonify(build_free())


@app.route("/json/paid")
def paid_json():

    from Utilities.Publishing.publisher import build_paid

    return jsonify(build_paid())

@app.route("/widget/rsi-pricesolver")
def widget_rsi_pricesolver():
    from EasyMode.RSI_PriceSolver.price_solver import render_page
    return render_page()

if __name__ == "__main__":
    app.run(debug=True)