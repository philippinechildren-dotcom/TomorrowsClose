from flask import render_template, request

from EasyMode.RSI_PriceSolver.rsi_solver import solve_rsi_price

from Utilities.market_data import (
    get_market_data,
    get_market_history,
)

from Utilities.order_rounding import (
    round_price_down_to_cent,
    round_price_up_to_cent,
)


def evaluate_rsi_pricesolver_mean_reversion(
    current_price: float,
    trigger_price: float,
) -> dict:

    if current_price < trigger_price:
        return {
            "status": "LONG",
            "zone_title": "SELL EXIT ZONE",
            "execution": "Sell Limit-on-Close",
            "trigger_price": round_price_up_to_cent(trigger_price),
        }

    return {
        "status": "FLAT",
        "zone_title": "BUY ENTRY ZONE",
        "execution": "Buy Limit-on-Close",
        "trigger_price": round_price_down_to_cent(trigger_price),
    }


def build_result(
    ticker="QQQ",
    rsi_period=3,
    threshold=30,
    dataset="homepage",
):

    ticker = ticker.upper()

    market_data = get_market_data(ticker)

    market_history = get_market_history(
        ticker=ticker,
        number_of_bars=500,
    )

    # Remove any missing closing prices (Yahoo occasionally returns a NaN row)
closing_prices = (
    market_history["close"]
    .dropna()
    .tolist()
)

if len(closing_prices) < 20:
    raise ValueError(
        f"Not enough valid closing prices returned for {ticker}."
    )

    signal = evaluate_rsi_pricesolver_mean_reversion(
        current_price=market_data["close"],
        trigger_price=solver_result["exact_price"],
    )

    result = {
        "dataset": dataset,
        "ticker": market_data["ticker"],
        "market_date": market_data["date"],
        "data_source": market_data["source"],
        "market_state": market_data["market_state"],
        "status": signal["status"],
        "trigger_price": signal["trigger_price"],
        "execution": signal["execution"],
        "rsi_period": rsi_period,
        "threshold": threshold,
    }

    return result


def render_page():

    ticker = request.args.get("ticker", "TQQQ")
    rsi_period = int(request.args.get("rsi_period", 3))
    threshold = int(request.args.get("threshold", 28))

    return render_template(
        "rsi_price_solver.html",
        result=build_result(
            ticker=ticker,
            rsi_period=rsi_period,
            threshold=threshold,
        ),
    )