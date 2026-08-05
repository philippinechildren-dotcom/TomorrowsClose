from StrategyLab.Strategies.ulcershield import build_result

result = build_result()

print(result["name"])
print(result["ending_equity"])
print(result["metrics"]["cagr"])
print(result["metrics"]["max_eod_drawdown"])
print(result["metrics"]["ulcer_performance_index"])