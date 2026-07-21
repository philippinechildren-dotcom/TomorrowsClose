from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, render_template, request

from market_data.provider import get_market_history
from indicators.rsi_pricesolver import solve_rsi_price
from strategies.rsi_pricesolver_mean_reversion import (
    evaluate_rsi_pricesolver_mean_reversion,
)

from shared.order_rounding import (
    round_down_cent,
    round_up_cent,
)

from metadata.strategies.rsi_pricesolver import STRATEGY_METADATA


app = Flask(__name__)


def build_result():

    defaults = STRATEGY_METADATA["default_parameters"]

    ticker = request.args.get(
        "ticker",
        defaults["ticker"]
    )

    rsi_period = int(
        request.args.get(
            "rsi_period",
            defaults["rsi_period"]
        )
    )

    threshold = int(
        request.args.get(
            "threshold",
            defaults["threshold"]
        )
    )

    history = get_market_history(
        ticker,
        bars=500
    )

    solver_result = solve_rsi_price(
        closes=history["close"],
        period=rsi_period,
        target=threshold
    )

    current_price = history["close"].iloc[-1]

    strategy_result = evaluate_rsi_pricesolver_mean_reversion(
        current_price=current_price,
        trigger_price=solver_result["exact_price"]
    )

    if strategy_result["rounding"] == "UP":

        trigger_price = round_up_cent(
            float(solver_result["exact_price"])
        )

    else:

        trigger_price = round_down_cent(
            float(solver_result["exact_price"])
        )


    market_date = history.index[-1].strftime(
        "%B %d, %Y"
    )

    calculation_time = (
        datetime.now(
            ZoneInfo("America/New_York")
        )
        .strftime("%I:%M %p ET")
    )


    return {

        "ticker": ticker,

        "rsi_period": rsi_period,

        "threshold": threshold,


        "current_price": round(
            float(current_price),
            2
        ),

        "trigger_price": trigger_price,


        "status": strategy_result["status"],

        "signal": strategy_result["signal"],

        "comparison": strategy_result["comparison"],

        "execution": strategy_result["execution"],


        "data_confidence": "★★★★★",

        "data_source": "Yahoo Finance",


        "last_updated": market_date,

        "last_updated_time": calculation_time,

    }



@app.route("/")
def home():

    return render_template(
        "index.html",
        result=build_result()
    )



@app.route("/calculate")
def calculate():

    return render_template(
        "index.html",
        result=build_result()
    )



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )