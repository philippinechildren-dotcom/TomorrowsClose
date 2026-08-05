from flask import render_template, request

from EasyMode.RSI_PriceSolver.price_solver import (
    build_result as build_rsi_result,
)

from EasyMode.LowHigh.price_solver import (
    build_result as build_lowhigh_result,
)

from EasyMode.UlcerShield.price_solver import (
    build_result as build_ulcershield_result,
)

def render_catalog():

    return render_template(
        "catalog.html",

        rsi_result=build_rsi_result(
            ticker=request.args.get("rsi_ticker", "TQQQ"),
            rsi_period=int(request.args.get("rsi_period", 3)),
            threshold=int(request.args.get("threshold", 28)),
        ),

        lowhigh_result=build_lowhigh_result(
            ticker=request.args.get("lowhigh_ticker", "QLD"),
            entry_lookback=int(request.args.get("entry_lookback", 3)),
            exit_lookback=int(request.args.get("exit_lookback", 1)),
        ),

        ulcershield_result=build_ulcershield_result(
            ticker=request.args.get("ulcershield_ticker", "TQQQ"),
            systems=[
                {
                    "name": "RSI1",
                    "period": int(request.args.get("period1", 2)),
                    "threshold": int(request.args.get("threshold1", 28)),
                },
                {
                    "name": "RSI2",
                    "period": int(request.args.get("period2", 3)),
                    "threshold": int(request.args.get("threshold2", 28)),
                },
                {
                    "name": "RSI3",
                    "period": int(request.args.get("period3", 5)),
                    "threshold": int(request.args.get("threshold3", 28)),
                },
                {
                    "name": "RSI4",
                    "period": int(request.args.get("period4", 8)),
                    "threshold": int(request.args.get("threshold4", 28)),
                },
                {
                    "name": "RSI5",
                    "period": int(request.args.get("period5", 13)),
                    "threshold": int(request.args.get("threshold5", 32)),
                },
            ],
        ),
    )