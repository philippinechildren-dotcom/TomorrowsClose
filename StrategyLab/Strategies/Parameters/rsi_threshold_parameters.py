"""
Strategy parameter widgets.
"""

from flask import render_template


def render_rsi_threshold_parameters():

    default_parameters = {
        "etf": "TQQQ",
        "rsi_period": 3,
        "threshold": 28,
    }

    return render_template(
        "display_components/strategy_lab/rsi_threshold_parameters.html",
        parameters=default_parameters,
    )