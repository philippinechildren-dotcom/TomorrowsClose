"""
Strategy parameter widgets.
"""

from flask import render_template


def render_rsi_threshold_parameters(
    etf="TQQQ",
    rsi_period=3,
    threshold=28,
    time_period="1_year",
):

    parameters = {
        "etf": etf,
        "rsi_period": rsi_period,
        "rsi_threshold": threshold,
        "time_period": time_period,
    }

    return render_template(
        "display_components/strategy_lab/rsi_threshold_parameters.html",
        parameters=parameters,
    )