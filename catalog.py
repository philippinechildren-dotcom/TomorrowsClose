from flask import render_template

from EasyMode.RSI_PriceSolver.price_solver import build_result


def render_catalog():

    return render_template(
        "catalog.html",
        result=build_result(),
    )