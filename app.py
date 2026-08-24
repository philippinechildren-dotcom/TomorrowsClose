import json

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

from EasyMode.TurnaroundTuesday.price_solver import (
    render_page as render_turnaround_tuesday_page,
)

from EasyMode.RSI_PriceSolver.price_solver import (
    render_page,
    build_result as build_rsi_result,
)

from EasyMode.UlcerShield.price_solver import (
    render_page as render_ulcershield_page,
)

from EasyMode.LowHigh_UlcerShield.price_solver import (
    render_page as render_lowhigh_ulcershield_page,
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

from StrategyLab.Strategies.turnaround_tuesday import (
    build_result as build_turnaround_tuesday_strategy,
)

from StrategyLab.Strategies.lowhigh_ulcershield import (
    build_result as build_lowhigh_ulcershield_strategy,
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

from StrategyLab.Strategies.Parameters.lowhigh_ulcershield_parameters import (
    render_lowhigh_ulcershield_parameters,
)

from PortfolioLab.portfolio_lab import build_portfolio_result, build_buy_and_hold

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

@app.route("/widget/portfolio-lab")
def portfolio_lab_widget():
    return render_template("display_components/portfolio_lab/portfolio_lab_dashboard.html")

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

@app.route("/widget/turnaround-tuesday")
def widget_turnaround_tuesday():
    return render_turnaround_tuesday_page()

@app.route("/widget/ulcershield")
def widget_ulcershield():
    return render_ulcershield_page()

@app.route("/widget/lowhigh-ulcershield")
def widget_lowhigh_ulcershield():
    return render_lowhigh_ulcershield_page()

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

    elif strategy_name == "turnaround_tuesday":

        strategy = build_turnaround_tuesday_strategy(
            ticker=etf,
            period=period,
            entry_lookback=int(
                request.args.get(
                    "entry_lookback",
                    1,
                )
            ),
        )

    elif strategy_name == "ulcershield":

        strategy = build_ulcershield_strategy(
            ticker=etf,
            period=period,
            rsi_1_period=int(
                request.args.get(
                    "rsi_1_period",
                    2,
                )
            ),
            rsi_1_threshold=int(
                request.args.get(
                    "rsi_1_threshold",
                    28,
                )
            ),
            rsi_2_period=int(
                request.args.get(
                    "rsi_2_period",
                    3,
                )
            ),
            rsi_2_threshold=int(
                request.args.get(
                    "rsi_2_threshold",
                    28,
                )
            ),
            rsi_3_period=int(
                request.args.get(
                    "rsi_3_period",
                    5,
                )
            ),
            rsi_3_threshold=int(
                request.args.get(
                    "rsi_3_threshold",
                    28,
                )
            ),
            rsi_4_period=int(
                request.args.get(
                    "rsi_4_period",
                    8,
                )
            ),
            rsi_4_threshold=int(
                request.args.get(
                    "rsi_4_threshold",
                    28,
                )
            ),
            rsi_5_period=int(
                request.args.get(
                    "rsi_5_period",
                    13,
                )
            ),
            rsi_5_threshold=int(
                request.args.get(
                    "rsi_5_threshold",
                    32,
                )
            ),
        )

    elif strategy_name == "lowhigh_ulcershield":
        
        strategy = build_lowhigh_ulcershield_strategy(
            ticker=etf,
            period=period,
            entry_lookback=int(
                request.args.get(
                    "entry_lookback",
                    1,
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
    legs_raw = request.args.get("legs")
    if legs_raw:
        try:
            legs = json.loads(legs_raw)
            rebalance = request.args.get("rebalance", "no_rebalance")
            period = request.args.get("period", "maximum")
            benchmark_ticker = request.args.get("benchmark_ticker", "QQQ")
            
            # 1. Compute portfolio result
            res = build_portfolio_result(
                legs=legs, 
                rebalance_schedule=rebalance, 
                period=period
            )

            # 2. Compute benchmark result
            bench_res = build_buy_and_hold(ticker=benchmark_ticker, period=period)

            eq_curve = res.get("equity_curve", [])
            dates = res.get("dates", [])
            bench_curve = bench_res.get("equity_curve", [])
            bench_dates = bench_res.get("dates", [])

            # 3. Align benchmark starting date to portfolio starting date
            if dates and bench_dates:
                start_date = dates[0]
                if start_date in bench_dates:
                    start_idx = bench_dates.index(start_date)
                    bench_curve = bench_curve[start_idx:]
                    bench_dates = bench_dates[start_idx:]

            # 4. Normalize both series to start at 0.0%
            start_eq = eq_curve[0] if eq_curve else 100000.0
            start_bench = bench_curve[0] if bench_curve else 100000.0

            chart_data = []
            min_len = min(len(eq_curve), len(bench_curve), len(dates))

            for i in range(min_len):
                strat_pct = ((eq_curve[i] - start_eq) / start_eq) * 100.0
                bench_pct = ((bench_curve[i] - start_bench) / start_bench) * 100.0
                chart_data.append({
                    "date": dates[i],
                    "strategy": strat_pct,
                    "benchmark": bench_pct
                })

            return jsonify({
                "strategy": "Portfolio Strategy",
                "benchmark": f"{benchmark_ticker} Buy & Hold",
                "chart_data": chart_data
            })
        except Exception as e:
            print(f"Error parsing portfolio performance chart: {e}")

    # ----------------------------------------------------
    # SINGLE STRATEGY FALLTHROUGH ROUTE
    # ----------------------------------------------------
    strategy = request.args.get("strategy", "rsi_threshold")
    
    # Check both 'etf' AND 'ticker' query parameters so SPY works properly
    etf = request.args.get("etf") or request.args.get("ticker") or "TQQQ"
    
    benchmark_ticker = request.args.get("benchmark_ticker", "QQQ")
    period = request.args.get("period", "maximum")

    # Fetch raw data from build_performance_chart
    if strategy == "lowhigh":
        raw_data = build_performance_chart(
            strategy="lowhigh",
            ticker=etf,
            period=period,
            benchmark_ticker=benchmark_ticker,
            entry_lookback=int(request.args.get("entry_lookback", 3)),
            exit_lookback=int(request.args.get("exit_lookback", 1)),
        )
    elif strategy == "turnaround_tuesday":
        raw_data = build_performance_chart(
            strategy="turnaround_tuesday",
            ticker=etf,
            period=period,
            benchmark_ticker=benchmark_ticker,
            entry_lookback=int(request.args.get("entry_lookback", 1)),
        )
    elif strategy == "ulcershield":
        raw_data = build_performance_chart(
            strategy="ulcershield",
            ticker=etf,
            period=period,
            benchmark_ticker=benchmark_ticker,
            rsi_1_period=int(request.args.get("rsi_1_period", 2)),
            rsi_1_threshold=int(request.args.get("rsi_1_threshold", 28)),
            rsi_2_period=int(request.args.get("rsi_2_period", 3)),
            rsi_2_threshold=int(request.args.get("rsi_2_threshold", 28)),
            rsi_3_period=int(request.args.get("rsi_3_period", 5)),
            rsi_3_threshold=int(request.args.get("rsi_3_threshold", 28)),
            rsi_4_period=int(request.args.get("rsi_4_period", 8)),
            rsi_4_threshold=int(request.args.get("rsi_4_threshold", 28)),
            rsi_5_period=int(request.args.get("rsi_5_period", 13)),
            rsi_5_threshold=int(request.args.get("rsi_5_threshold", 32)),
        )
    elif strategy == "lowhigh_ulcershield":
        raw_data = build_performance_chart(
            strategy="lowhigh_ulcershield",
            ticker=etf,
            period=period,
            benchmark_ticker=benchmark_ticker,
            entry_lookback=int(request.args.get("entry_lookback", 1)),
            exit_lookback=int(request.args.get("exit_lookback", 1)),
        )
    else:
        raw_data = build_performance_chart(
            strategy="rsi_threshold",
            ticker=etf,
            period=period,
            benchmark_ticker=benchmark_ticker,
            rsi_length=int(request.args.get("rsi_period", 3)),
            rsi_threshold=int(request.args.get("rsi_threshold", 28)),
        )

    # Re-base single-strategy response starting strictly at 0.0%
    if isinstance(raw_data, dict) and "chart_data" in raw_data:
        c_data = raw_data["chart_data"]
        valid_points = [p for p in c_data if p.get("strategy") is not None and p.get("benchmark") is not None]
        if valid_points:
            start_strat = valid_points[0]["strategy"]
            start_bench = valid_points[0]["benchmark"]
            
            for p in valid_points:
                p["strategy"] = round(p["strategy"] - start_strat, 2)
                p["benchmark"] = round(p["benchmark"] - start_bench, 2)
                
            raw_data["chart_data"] = valid_points

    return jsonify(raw_data)

@app.route("/json/annual-returns")
def annual_returns_json():

    legs_raw = request.args.get("legs")
    if legs_raw:
        try:
            legs = json.loads(legs_raw)
            rebalance = request.args.get("rebalance", "no_rebalance")
            period = request.args.get("period", "maximum")

            res = build_portfolio_result(
                legs=legs, rebalance_schedule=rebalance, period=period
            )

            # Check if portfolio lab returned pre-computed annual returns
            if "annual_returns" in res and res["annual_returns"]:
                portfolio_annuals = res["annual_returns"]
            else:
                # Fallback: compute annual returns directly from dates and equity curve
                dates = res.get("dates", [])
                equity_curve = res.get("equity_curve", [])
                yearly_data = {}

                for d, eq in zip(dates, equity_curve):
                    yr = int(d[:4])
                    if yr not in yearly_data:
                        yearly_data[yr] = []
                    yearly_data[yr].append(eq)

                portfolio_annuals = []
                for yr, values in yearly_data.items():
                    start_val = values[0]
                    end_val = values[-1]
                    year_ret = (end_val - start_val) / start_val

                    peak = values[0]
                    max_dd = 0.0
                    for val in values:
                        if val > peak:
                            peak = val
                        dd = (val - peak) / peak
                        if dd < max_dd:
                            max_dd = dd

                    portfolio_annuals.append(
                        {
                            "year": yr,
                            "return": year_ret,
                            "max_eod_drawdown": abs(max_dd),
                        }
                    )

            return jsonify(
                {
                    "strategy": "Portfolio Strategy",
                    "annual_returns": portfolio_annuals[::-1],
                }
            )

        except Exception as e:
            print(f"ERROR IN PORTFOLIO ANNUAL RETURNS: {e}")

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

        strategy_result = build_lowhigh_strategy(
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

    elif strategy == "turnaround_tuesday":

        strategy_result = build_turnaround_tuesday_strategy(
            ticker=etf,
            period=period,
            entry_lookback=int(
                request.args.get(
                    "entry_lookback",
                    1,
                )
            ),
        )

    elif strategy == "ulcershield":

        strategy_result = build_ulcershield_strategy(
            ticker=etf,
            period=period,
            rsi_1_period=int(
                request.args.get(
                    "rsi_1_period",
                    2,
                )
            ),
            rsi_1_threshold=int(
                request.args.get(
                    "rsi_1_threshold",
                    28,
                )
            ),
            rsi_2_period=int(
                request.args.get(
                    "rsi_2_period",
                    3,
                )
            ),
            rsi_2_threshold=int(
                request.args.get(
                    "rsi_2_threshold",
                    28,
                )
            ),
            rsi_3_period=int(
                request.args.get(
                    "rsi_3_period",
                    5,
                )
            ),
            rsi_3_threshold=int(
                request.args.get(
                    "rsi_3_threshold",
                    28,
                )
            ),
            rsi_4_period=int(
                request.args.get(
                    "rsi_4_period",
                    8,
                )
            ),
            rsi_4_threshold=int(
                request.args.get(
                    "rsi_4_threshold",
                    28,
                )
            ),
            rsi_5_period=int(
                request.args.get(
                    "rsi_5_period",
                    13,
                )
            ),
            rsi_5_threshold=int(
                request.args.get(
                    "rsi_5_threshold",
                    32,
                )
            ),
        )

    elif strategy == "lowhigh_ulcershield":
    
        strategy_result = build_lowhigh_ulcershield_strategy(
            ticker=etf,
            period=period,
            entry_lookback=int(
                request.args.get(
                    "entry_lookback",
                    1,
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

        strategy_result = build_rsi_strategy(
            ticker=etf,
            period=period,
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

    legs_raw = request.args.get("legs")
    period = request.args.get("period", "maximum")
    rebalance = request.args.get("rebalance", "no_rebalance")

    if legs_raw:
        try:
            legs = json.loads(legs_raw)
            portfolio_res = build_portfolio_result(
                legs=legs,
                rebalance_schedule=rebalance,
                period=period
            )
            # portfolio_res already contains "metrics" and top-level metric keys
            return render_small_metrics_page(
                strategy=portfolio_res,
                selected_period=period,
            )
        except Exception as e:
            print(f"Error evaluating portfolio legs in small metrics: {e}")

    # Fallback to default Buy & Hold QQQ if no legs are passed
    from PortfolioLab.portfolio_lab import build_buy_and_hold
    default_strat = build_buy_and_hold(ticker="QQQ", period=period)
    
    return render_small_metrics_page(
        strategy=default_strat,
        selected_period=period,
    )

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

    elif strategy_name == "turnaround_tuesday":

        strategy = build_turnaround_tuesday_strategy(
            ticker=etf,
            period=period,
            entry_lookback=int(
                request.args.get(
                    "entry_lookback",
                    1,
                )
            ),
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

    elif strategy_name == "turnaround_tuesday":

        strategy = build_turnaround_tuesday_strategy(
            ticker=etf,
            period=period,
            entry_lookback=int(
                request.args.get(
                    "entry_lookback",
                    1,
                )
            ),
        )

    elif strategy_name == "ulcershield":

        strategy = build_ulcershield_strategy(
            ticker=etf,
            period=period,
            rsi_1_period=int(
                request.args.get(
                    "rsi_1_period",
                    2,
                )
            ),
            rsi_1_threshold=int(
                request.args.get(
                    "rsi_1_threshold",
                    28,
                )
            ),
            rsi_2_period=int(
                request.args.get(
                    "rsi_2_period",
                    3,
                )
            ),
            rsi_2_threshold=int(
                request.args.get(
                    "rsi_2_threshold",
                    28,
                )
            ),
            rsi_3_period=int(
                request.args.get(
                    "rsi_3_period",
                    5,
                )
            ),
            rsi_3_threshold=int(
                request.args.get(
                    "rsi_3_threshold",
                    28,
                )
            ),
            rsi_4_period=int(
                request.args.get(
                    "rsi_4_period",
                    8,
                )
            ),
            rsi_4_threshold=int(
                request.args.get(
                    "rsi_4_threshold",
                    28,
                )
            ),
            rsi_5_period=int(
                request.args.get(
                    "rsi_5_period",
                    13,
                )
            ),
            rsi_5_threshold=int(
                request.args.get(
                    "rsi_5_threshold",
                    32,
                )
            ),
        )

    elif strategy_name == "lowhigh_ulcershield":
    
        strategy = build_lowhigh_ulcershield_strategy(
            ticker=etf,
            period=period,
            entry_lookback=int(
                request.args.get(
                    "entry_lookback",
                    1,
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

@app.route("/widget/turnaround-tuesday-parameters")
def widget_turnaround_tuesday_parameters():

    return render_template(
        "display_components/strategy_lab/turnaround_tuesday_parameters.html",
        parameters={
            "etf": request.args.get("etf", "QQQ"),
            "entry_lookback": int(
                request.args.get("entry_lookback", 1)
            ),
            "period": request.args.get(
                "period",
                "maximum",
            ),
        },
    )


@app.route("/widget/turnaround-tuesday-dashboard")
def widget_turnaround_tuesday_dashboard():

    return render_template(
        "display_components/strategy_lab/turnaround_tuesday_dashboard.html",
        parameters={
            "etf": request.args.get("etf", "QQQ"),
            "entry_lookback": int(
                request.args.get("entry_lookback", 1)
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

@app.route("/widget/ulcershield-dashboard")
def widget_ulcershield_dashboard():

    return render_template(
        "display_components/strategy_lab/ulcershield_dashboard.html",
        parameters={
            "etf": request.args.get("etf", "TQQQ"),

            "rsi_1_period": int(
                request.args.get("rsi_1_period", 2)
            ),
            "rsi_1_threshold": int(
                request.args.get("rsi_1_threshold", 28)
            ),

            "rsi_2_period": int(
                request.args.get("rsi_2_period", 3)
            ),
            "rsi_2_threshold": int(
                request.args.get("rsi_2_threshold", 28)
            ),

            "rsi_3_period": int(
                request.args.get("rsi_3_period", 5)
            ),
            "rsi_3_threshold": int(
                request.args.get("rsi_3_threshold", 28)
            ),

            "rsi_4_period": int(
                request.args.get("rsi_4_period", 8)
            ),
            "rsi_4_threshold": int(
                request.args.get("rsi_4_threshold", 28)
            ),

            "rsi_5_period": int(
                request.args.get("rsi_5_period", 13)
            ),
            "rsi_5_threshold": int(
                request.args.get("rsi_5_threshold", 32)
            ),

            "period": request.args.get(
                "period",
                "maximum",
            ),
        },
    )

@app.route("/widget/lowhigh-ulcershield-parameters")
def widget_lowhigh_ulcershield_parameters():

    return render_lowhigh_ulcershield_parameters(
        etf=request.args.get("etf", "QQQ"),
        entry_lookback=int(
            request.args.get("entry_lookback", 1)
        ),
        exit_lookback=int(
            request.args.get("exit_lookback", 1)
        ),
        time_period=request.args.get(
            "period",
            "maximum",
        ),
    )

@app.route("/widget/lowhigh-ulcershield-dashboard")
def widget_lowhigh_ulcershield_dashboard():

    return render_template(
        "display_components/strategy_lab/lowhigh_ulcershield_dashboard.html",
        parameters={
            "etf": request.args.get("etf", "QQQ"),
            "entry_lookback": int(
                request.args.get("entry_lookback", 1)
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

@app.route("/widget/portfolio-lab-dashboard")
def widget_portfolio_lab_dashboard():
    default_legs = [
        {"strategy": "buy_and_hold", "etf": "QQQ", "allocation": 25},
        {"strategy": "lowhigh", "etf": "QQQ", "allocation": 25},
        {"strategy": "ulcershield", "etf": "QQQ", "allocation": 25},
        {"strategy": "buy_and_hold", "etf": "TQQQ", "allocation": 25},
    ]
    return render_template(
        "display_components/portfolio_lab/portfolio_lab_dashboard.html",
        legs=default_legs,
        rebalance="no_rebalance",
        period="maximum",
    )


@app.route("/json/portfolio-lab-metrics", methods=["POST"])
def portfolio_lab_metrics():
    payload = request.get_json() or {}
    legs = payload.get("legs", [])
    period = payload.get("period", "maximum")
    rebalance = payload.get("rebalance", "no_rebalance")

    result = build_portfolio_result(
        legs=legs, rebalance_schedule=rebalance, period=period
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)