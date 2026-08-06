from StrategyLab.Strategies.lowhigh import build_result

result = build_result(
    ticker="QLD",
    period="maximum",
)

metrics = result["metrics"]

print(result["name"])
print(f"Ending Equity: {result['ending_equity']:,.0f}")
print(f"CAGR: {metrics['cagr']:.2%}")
print(f"Exposure: {metrics['exposure']:.2%}")
print(f"Trades: {metrics['number_of_trades']}")
print(f"Max EOD DD: {metrics['max_eod_drawdown']:.2%}")
print(f"Max Closed DD: {metrics['max_closed_trade_drawdown']:.2%}")
print(f"UPI: {metrics['ulcer_performance_index']:.2f}")