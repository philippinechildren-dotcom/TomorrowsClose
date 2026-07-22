from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, render_template, request

from market_data.provider import get_market_history

from indicators.rsi_pricesolver import solve_rsi_price

from strategies.rsi_pricesolver_mean_reversion import (
    evaluate_rsi_pricesolver_mean_reversion,
)

from pages.rsi_pricesolver import (
    build_result,
)

from strategies.ulcershield import (
    calculate_ulcershield,
)

from pages.ulcershield import (
    build_result as build_ulcershield_result,
)

from strategies.lowhigh import (
    calculate_lowhigh,
)

from pages.lowhigh import (
    build_result as build_lowhigh_result,
)

from shared.order_rounding import (
    round_down_cent,
    round_up_cent,
)

from catalog.strategies import get_strategy
from catalog.indicators import get_indicator


app = Flask(__name__)

from shared.formatting import (
    format_price,
)

app.jinja_env.filters["price"] = format_price

@app.route("/")
def home():

    return render_template(
        "rsi_pricesolver.html",
        result=build_result()
    )


@app.route("/calculate")
def calculate():

    return render_template(
        "rsi_pricesolver.html",
        result=build_result()
    )


@app.route("/ulcershield")
def ulcershield():

    return render_template(
        "ulcershield.html",
        result=build_ulcershield_result()
    )

@app.route("/lowhigh")
def lowhigh():

    return render_template(
        "lowhigh.html",
        result=build_lowhigh_result()
    )

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )