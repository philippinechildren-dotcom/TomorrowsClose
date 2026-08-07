"""
StrategyLab/Metrics/Tables/small_metrics.py
"""

from flask import render_template


def render_page(
    strategy,
    selected_period,
):
    """
    Render the Small Metrics widget.
    """

    return render_template(
        "display_components/performance/small_metrics.html",
        strategy=strategy,
        metrics=strategy["metrics"],
        selected_period=selected_period,
    )