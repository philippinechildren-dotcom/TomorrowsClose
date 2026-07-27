performance_result = build_rsi_pricesolver(
    ticker=ticker,
    rsi_length=rsi_period,
    threshold=threshold,
    period=period,
)

performance = calculate_performance(
    performance_result["equity_curve"],
    performance_result.get("closed_equity"),
)

benchmark_result = build_buy_and_hold(
    ticker="QQQ",
    period=period,
)

benchmark_result["performance"] = calculate_performance(
    benchmark_result["equity_curve"],
)