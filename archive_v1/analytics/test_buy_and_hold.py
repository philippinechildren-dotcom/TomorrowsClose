from analytics.strategies.build_buy_and_hold import build_buy_and_hold

result = build_buy_and_hold("QQQ")

print()

for key, value in result.items():

    if key not in ("equity_curve", "drawdowns"):

        print(f"{key}: {value}")

print()

print(f"Equity curve length: {len(result['equity_curve'])}")

print()

print("First 10 drawdowns:")

for dd in result["drawdowns"][:10]:

    print(dd)

print()

print("Maximum drawdown:")

print(max(result["drawdowns"]))