import json
from flask import render_template


def render_page():
    """
    Render the Rankings widget page with initial json dataset.
    """
    with open("Rankings/rankings.json", "r") as f:
        rankings_data = json.load(f)

    return render_template(
        "display_components/rankings/rankings_widget.html",
        initial_data=json.dumps(rankings_data),
    )