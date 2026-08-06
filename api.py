from flask import (
    Flask,
    send_file,
    request,
)
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

from Rankings.page import (
    render_page as render_rankings_page,
)

from StrategyLab.Strategies.rsi_threshold import (
    build_result as build_rsi_strategy,
)

from StrategyLab.Metrics.Tables.full_metrics import (
    render_page as render_full_metrics_page,
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


@app.route("/widget/rankings")
def widget_rankings():
    return render_rankings_page()


@app.route("/widget/full-metrics")
def widget_full_metrics():

    period = request.args.get(
        "period",
        default=1.0,
        type=float,
    )

    strategy = build_rsi_strategy(
        ticker="TQQQ",
        period=period,
        rsi_length=3,
        rsi_threshold=28,
    )

    return render_full_metrics_page(
        strategy=strategy,
        selected_period=period,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)