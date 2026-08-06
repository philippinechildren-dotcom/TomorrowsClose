"""
StrategyLab/Metrics/Tables/full_metrics.py
"""

from flask import render_template


def render_page(
    strategy,
    selected_period,
):
    """
    Render the Full Metrics table.
    """

    return render_template(
        "display_components/performance/full_metrics.html",
        strategy=strategy,
        metrics=strategy["metrics"],
        selected_period=selected_period,
    )