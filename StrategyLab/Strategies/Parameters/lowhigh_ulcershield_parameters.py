"""
Strategy parameter widgets.
"""

from flask import render_template


def render_lowhigh_ulcershield_parameters(
    etf="QQQ",
    entry_lookback=1,
    exit_lookback=1,
    time_period="maximum",
):

    parameters = {
        "etf": etf,
        "entry_lookback": entry_lookback,
        "exit_lookback": exit_lookback,
        "time_period": time_period,
    }

    return render_template(
        "display_components/strategy_lab/lowhigh_ulcershield_parameters.html",
        parameters=parameters,
    )