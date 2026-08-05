from flask import render_template


def render_page():

    return render_template(
        "display_components/rankings/rankings.html",
    )