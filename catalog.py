from flask import render_template, request

from EasyMode.RSI_PriceSolver.price_solver import build_result


def render_catalog():

    ticker = request.args.get("ticker", "QQQ")
    rsi_period = int(request.args.get("rsi_period", 3))
    threshold = float(request.args.get("threshold", 30))

    return render_template(
        "catalog.html",
        result=build_result(
            ticker=ticker,
            rsi_period=rsi_period,
            threshold=threshold,
        ),
    )