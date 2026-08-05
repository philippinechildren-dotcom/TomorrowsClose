from flask import Flask, send_file
from flask_cors import CORS

from EasyMode.RSI_PriceSolver.price_solver import (
    render_page as render_rsi_page,
)

from EasyMode.LowHigh.price_solver import (
    render_page as render_lowhigh_page,
)

from EasyMode.UlcerShield.price_solver import (
    render_page as render_ulcershield_page,
)

app = Flask(__name__)
CORS(app)


@app.route("/widget/rsi-pricesolver")
def widget_rsi_pricesolver():
    return render_rsi_page()


@app.route("/widget/lowhigh")
def widget_lowhigh():
    return render_lowhigh_page()


@app.route("/widget/ulcershield")
def widget_ulcershield():
    return render_ulcershield_page()


@app.route("/json/rankings")
def rankings_json():
    return send_file(
        "Rankings/rankings.json",
        mimetype="application/json",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)