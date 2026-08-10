from flask import (
    Flask,
    render_template,
    jsonify,
    send_file,
    request,
)

from catalog import render_catalog

from EasyMode.LowHigh.price_solver import (
    render_page as render_lowhigh_page,
)

from EasyMode.RSI_PriceSolver.price_solver import (
    render_page,
    build_result as build_rsi_result,
)

from EasyMode.UlcerShield.price_solver import (
    render_page as render_ulcershield_page,
)

from Rankings.page import (
    render_page as render_rankings_page,
)

from StrategyLab.Strategies.rsi_threshold import (
    build_result as build_rsi_strategy,
)

from StrategyLab.Strategies.lowhigh import (
    build_result as build_lowhigh_strategy,
)

from StrategyLab.Strategies.ulcershield import (
    build_result as build_ulcershield_strategy,
)

from StrategyLab.Metrics.Tables.full_metrics import (
    render_page as render_full_metrics_page,
)

from StrategyLab.Charts.performance_chart import (
    build_performance_chart,
)

from StrategyLab.Metrics.Tables.annual_returns import (
    build_annual_returns,
)

from StrategyLab.Metrics.Tables.small_metrics import (
    render_page as render_small_metrics_page,
)

from StrategyLab.Strategies.Parameters.rsi_threshold_parameters import (
    render_rsi_threshold_parameters,
)

app = Flask(__name__)


@app.route("/")
def catalog():
    return render_catalog()


@app.route("/prototype")
def prototype():
    return render_template("homepage_test.html")


@app.route("/json/homepage")
def homepage_json():
    from Utilities.Publishing.publisher import build_homepage
    return jsonify(build_homepage())


@app.route("/json/rankings")
def rankings_json():
    return send_file(
        "Rankings/rankings.json",
        mimetype="application/json",
    )


@app.route("/widget/rsi-pricesolver")
def widget_rsi_pricesolver():
    return render_page()


@app.route("/widget/lowhigh")
def widget_lowhigh():
    return render_lowhigh_page()


@app.route("/widget/ulcershield")
def widget_ulcershield():
    return render_ulcershield_page()


@app.route("/widget/rankings")
def widget_rankings():
    return render_rankings_page()


@app.route("/widget/full-metrics")
def widget_full_metrics():

    etf = request.args.get(
        "etf",
        "TQQQ",
    )

    rsi_period = int(
        request.args.get(
            "rsi_period",
            3,
        )
    )

    rsi_threshold = int(
        request.args.get(
            "rsi_threshold",
            28,
        )
    )

    period = request.args.get(
        "period",
        "maximum",
    )

    strategy = build_rsi_strategy(
        ticker=etf,
        period=period,
        rsi_length=rsi_period,
        rsi_threshold=rsi_threshold,
    )

    return render_full_metrics_page(
        strategy=strategy,
        selected_period=period,
    )

@app.route("/widget/market-data-confidence")
def widget_market_data_confidence():
    return render_template(
        "display_components/data/widget_market_data_confidence.html",
        result=build_rsi_result(dataset="homepage"),
    )


@app.route("/widget/homepage-rsi-pricesolver")
def widget_homepage_rsi_pricesolver():
    return render_template(
        "display_components/pricesolvers/homepage_rsi_pricesolver.html",
        result=build_rsi_result(dataset="homepage"),
    )

@app.route("/widget/performance-chart")
def performance_chart_widget():

    return render_template(
        "display_components/performance/performance_chart.html"
    )

@app.route("/json/performance-chart")
def performance_chart_json():

    etf = request.args.get(
        "etf",
        "TQQQ",
    )

    rsi_period = int(
        request.args.get(
            "rsi_period",
            3,
        )
    )

    rsi_threshold = int(
        request.args.get(
            "rsi_threshold",
            28,
        )
    )

    period = request.args.get(
        "period",
        default=None,
    )

    period = request.args.get(
    "period",
    default="maximum",
)

    return jsonify(
        build_performance_chart(
            strategy="rsi_threshold",
            ticker=etf,
            period=period,
            rsi_length=rsi_period,
            rsi_threshold=rsi_threshold,
        )
    )

    return jsonify(
        build_performance_chart(
            strategy="rsi_threshold",
            ticker=etf,
            period=period,
            rsi_length=rsi_period,
            rsi_threshold=rsi_threshold,
        )
    )

@app.route("/json/annual-returns")
def annual_returns_json():

    strategy = request.args.get(
        "strategy",
        "rsi_threshold",
    )

    etf = request.args.get(
        "etf",
        "TQQQ",
    )

    rsi_period = int(
        request.args.get(
            "rsi_period",
            3,
        )
    )

    rsi_threshold = int(
        request.args.get(
            "rsi_threshold",
            28,
        )
    )

    strategy_builders = {
        "ulcershield": build_ulcershield_strategy,
        "rsi_threshold": build_rsi_strategy,
        "lowhigh": build_lowhigh_strategy,
    }

    if strategy == "rsi_threshold":

        strategy_result = build_rsi_strategy(
            ticker=etf,
            rsi_length=rsi_period,
            rsi_threshold=rsi_threshold,
        )

    else:

        strategy_result = strategy_builders[strategy](
            ticker=etf,
        )

    annual_returns = build_annual_returns(
        strategy_result
    )

    return jsonify(
        {
            "strategy": strategy_result["name"],
            "annual_returns": annual_returns,
        }
    )

@app.route("/widget/annual-returns")
def annual_returns_widget():

    return render_template(
        "display_components/performance/annual_returns.html"
    )

@app.route("/widget/small-metrics")
def widget_small_metrics():

    etf = request.args.get(
        "etf",
        "TQQQ",
    )

    rsi_period = int(
        request.args.get(
            "rsi_period",
            3,
        )
    )

    threshold = int(
        request.args.get(
            "threshold",
            28,
        )
    )

    period = request.args.get(
        "period",
        "1_year",
    )

    strategy = build_rsi_strategy(
        ticker=etf,
        period=period,
        rsi_length=rsi_period,
        rsi_threshold=threshold,
    )

    return render_small_metrics_page(
        strategy=strategy,
        selected_period=period,
    )

@app.route("/json/small-metrics")
def json_small_metrics():

    etf = request.args.get(
        "etf",
        "TQQQ",
    )

    rsi_period = int(
        request.args.get(
            "rsi_period",
            3,
        )
    )

    threshold = int(
        request.args.get(
            "rsi_threshold",
            28,
        )
    )

    period = request.args.get(
        "period",
        "maximum",
    )

    strategy = build_rsi_strategy(
        ticker=etf,
        period=period,
        rsi_length=rsi_period,
        rsi_threshold=threshold,
    )

    return jsonify(
        {
            "metrics": strategy["metrics"],
        }
    )

@app.route("/widget/rsi-threshold-parameters")
def widget_rsi_threshold_parameters():
    return render_rsi_threshold_parameters()

if __name__ == "__main__":
    app.run(debug=True)