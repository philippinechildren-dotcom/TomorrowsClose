from flask import render_template


def render_page(
    strategy,
    selected_period,
):
    """
    Render the Small Metrics widget.
    """
    
    metrics_data = strategy.get("metrics") if isinstance(strategy, dict) else None
    if metrics_data is None and isinstance(strategy, dict):
        metrics_data = strategy

    return render_template(
        "display_components/performance/small_metrics.html",
        strategy=strategy,
        metrics=metrics_data,
        selected_period=selected_period,
    )