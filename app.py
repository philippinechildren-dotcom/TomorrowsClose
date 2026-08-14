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

from StrategyLab.Strategies.Parameters.lowhigh_parameters import (
    render_lowhigh_parameters,
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

    strategy_name = request.args.get(
        "strategy",
        "rsi_threshold",
    )

    etf = request.args.get(
        "etf",
        "TQQQ",
    )

    period = request.args.get(
        "period",
        "maximum",
    )

    if strategy_name == "lowhigh":

        strategy = build_lowhigh_strategy(
            ticker=etf,
            period=period,
            entry_lookback=int(
                request.args.get(
                    "entry_lookback",
                    3,
                )
            ),
            exit_lookback=int(
                request.args.get(
                    "exit_lookback",
                    1,
                )
            ),
        )

    else:

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

    strategy = request.args.get(
        "strategy",
        "rsi_threshold",
    )

    etf = request.args.get(
        "etf",
        "TQQQ",
    )

    period = request.args.get(
        "period",
        "maximum",
    )

    if strategy == "lowhigh":

        return jsonify(
            build_performance_chart(
                strategy="lowhigh",
                ticker=etf,
                period=period,
            )
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

    if strategy == "lowhigh":

        strategy_result = build_lowhigh_strategy(
            ticker=etf,
            entry_lookback=int(
                request.args.get(
                    "entry_lookback",
                    3,
                )
            ),
            exit_lookback=int(
                request.args.get(
                    "exit_lookback",
                    1,
                )
            ),
        )

    elif strategy == "ulcershield":

        strategy_result = build_ulcershield_strategy(
            ticker=etf,
        )

    else:

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

        strategy_result = build_rsi_strategy(
            ticker=etf,
            rsi_length=rsi_period,
            rsi_threshold=rsi_threshold,
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
def small_metrics_widget():

    strategy_name = request.args.get("strategy")

    etf = request.args.get(
        "etf",
        "TQQQ",
    )

    period = request.args.get(
        "period",
        "maximum",
    )

    if strategy_name == "lowhigh":

        strategy = build_lowhigh_strategy(
            ticker=etf,
            period=period,
            entry_lookback=int(
                request.args.get(
                    "entry_lookback",
                    3,
                )
            ),
            exit_lookback=int(
                request.args.get(
                    "exit_lookback",
                    1,
                )
            ),
        )

    elif strategy_name == "rsi_threshold":

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

        strategy = build_rsi_strategy(
            ticker=etf,
            period=period,
            rsi_length=rsi_period,
            rsi_threshold=threshold,
        )

    else:

        strategy = {
            "name": "",
            "metrics": None,
        }

    return render_small_metrics_page(
        strategy=strategy,
        selected_period=period,
    )

@app.route("/json/small-metrics")
def json_small_metrics():

    strategy_name = request.args.get("strategy")

    etf = request.args.get(
        "etf",
        "TQQQ",
    )

    period = request.args.get(
        "period",
        "maximum",
    )

    if strategy_name == "lowhigh":

        strategy = build_lowhigh_strategy(
            ticker=etf,
            period=period,
            entry_lookback=int(
                request.args.get(
                    "entry_lookback",
                    3,
                )
            ),
            exit_lookback=int(
                request.args.get(
                    "exit_lookback",
                    1,
                )
            ),
        )

    elif strategy_name == "rsi_threshold":

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

        strategy = build_rsi_strategy(
            ticker=etf,
            period=period,
            rsi_length=rsi_period,
            rsi_threshold=threshold,
        )

    else:

        return jsonify(
            {
                "strategy": None,
                "metrics": None,
            }
        )

    return jsonify(
        {
            "strategy": strategy["name"],
            "metrics": strategy["metrics"],
        }
    )

@app.route("/widget/rsi-threshold-parameters")
def widget_rsi_threshold_parameters():
    return render_rsi_threshold_parameters()

@app.route("/widget/metric-selection")
def metric_selection_widget():
    return render_template(
        "display_components/strategy_lab/metric_selection.html"
    )

@app.route("/widget/lowhigh-parameters")
def widget_lowhigh_parameters():

    return render_lowhigh_parameters(
        etf=request.args.get("etf", "QLD"),
        entry_lookback=int(
            request.args.get("entry_lookback", 3)
        ),
        exit_lookback=int(
            request.args.get("exit_lookback", 1)
        ),
        time_period=request.args.get(
            "period",
            "maximum",
        ),
    )

@app.route("/widget/lowhigh-dashboard")
def widget_lowhigh_dashboard():

    return render_template(
        "display_components/strategy_lab/lowhigh_dashboard.html",
        parameters={
            "etf": request.args.get("etf", "QLD"),
            "entry_lookback": int(
                request.args.get("entry_lookback", 3)
            ),
            "exit_lookback": int(
                request.args.get("exit_lookback", 1)
            ),
            "period": request.args.get(
                "period",
                "maximum",
            ),
        },
    )

@app.route("/widget/rsi-threshold-dashboard")
def widget_rsi_threshold_dashboard():

    return render_template(
        "display_components/strategy_lab/rsi_threshold_dashboard.html",
        parameters={
            "etf": request.args.get("etf", "TQQQ"),
            "rsi_period": int(
                request.args.get("rsi_period", 3)
            ),
            "rsi_threshold": int(
                request.args.get("rsi_threshold", 28)
            ),
            "period": request.args.get(
                "period",
                "maximum",
            ),
        },
    )

if __name__ == "__main__":
    app.run(debug=True)