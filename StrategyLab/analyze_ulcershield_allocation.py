import yfinance as yf
import pandas as pd

RSI_SYSTEMS = [
    (2, 28),
    (3, 28),
    (5, 28),
    (8, 28),
    (13, 32),
]

ALLOCATION_PER_SYSTEM = 20.0


def calculate_rsi(prices, period):
    delta = prices.diff()

    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    avg_gain = gains.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False
    ).mean()

    avg_loss = losses.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


# ---------------------------------------------------------
# Load TQQQ history
# ---------------------------------------------------------

data = yf.download(
    "TQQQ",
    period="max",
    interval="1d",
    auto_adjust=False,
    progress=False
)

close = data["Close"]

if isinstance(close, pd.DataFrame):
    close = close.iloc[:, 0]

# ---------------------------------------------------------
# Calculate RSI values
# ---------------------------------------------------------

rsi_values = []

for period, threshold in RSI_SYSTEMS:
    rsi_values.append(calculate_rsi(close, period))

# ---------------------------------------------------------
# Track positions and allocation
# ---------------------------------------------------------

in_position = [False] * 5

allocation_counts = {
    0: 0,
    20: 0,
    40: 0,
    60: 0,
    80: 0,
    100: 0
}

# Each RSI system starts with 20% of total capital.
system_equity = [20000.0] * 5

total_equity = 100000.0
peak_equity = total_equity

allocation_drawdowns = {
    0: [],
    20: [],
    40: [],
    60: [],
    80: [],
    100: []
}

previous_close = None

# ---------------------------------------------------------
# Process every trading day
# ---------------------------------------------------------

for date in close.index:

    current_close = close.loc[date]

    if pd.isna(current_close):
        continue

    # -----------------------------------------------------
    # First apply today's market return to positions that
    # were already open BEFORE today's close.
    #
    # This matches process_orders_on_close behavior:
    # today's new entry does not receive today's return.
    # -----------------------------------------------------

    if previous_close is not None:

        daily_return = (
            current_close / previous_close
        ) - 1

        for i in range(5):

            if in_position[i]:
                system_equity[i] *= (
                    1 + daily_return
                )

        total_equity = sum(system_equity)

        peak_equity = max(
            peak_equity,
            total_equity
        )

    # -----------------------------------------------------
    # Update today's RSI position states
    # -----------------------------------------------------

    for i, (period, threshold) in enumerate(RSI_SYSTEMS):

        rsi = rsi_values[i].loc[date]

        if pd.isna(rsi):
            continue

        if not in_position[i] and rsi < threshold:
            in_position[i] = True

        elif in_position[i] and rsi > threshold:
            in_position[i] = False

    # -----------------------------------------------------
    # Determine end-of-day allocation
    # -----------------------------------------------------

    active_systems = sum(in_position)

    allocation = (
        active_systems * ALLOCATION_PER_SYSTEM
    )

    allocation_counts[allocation] += 1

    # -----------------------------------------------------
    # Record drawdown at this allocation level
    # -----------------------------------------------------

    drawdown = (
        (peak_equity - total_equity)
        / peak_equity
        * 100
    )

    allocation_drawdowns[allocation].append(
        drawdown
    )

    previous_close = current_close


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

total_days = sum(allocation_counts.values())

weighted_allocation = 0

print()
print("=" * 60)
print("ULCERSHIELD ALLOCATION ANALYSIS")
print("=" * 60)
print()

print("ALLOCATION DISTRIBUTION")
print("-" * 60)

for allocation, days in allocation_counts.items():

    pct = days / total_days * 100

    weighted_allocation += (
        allocation * days
    )

    print(
        f"{allocation:>3}% allocation: "
        f"{days:>6,} days "
        f"({pct:>6.2f}%)"
    )

average_allocation = (
    weighted_allocation / total_days
)

print()
print("-" * 60)

print(
    f"Average capital utilization: "
    f"{average_allocation:.2f}%"
)

print(
    f"Average capital idle: "
    f"{100 - average_allocation:.2f}%"
)

# ---------------------------------------------------------
# Drawdown by allocation level
# ---------------------------------------------------------

print()
print("NAV DRAWDOWN BY ALLOCATION")
print("-" * 60)

for allocation in allocation_counts:

    drawdowns = allocation_drawdowns[allocation]

    if drawdowns:

        max_drawdown = max(drawdowns)
        average_drawdown = sum(drawdowns) / len(drawdowns)

        print(
            f"{allocation:>3}% allocation: "
            f"Max DD {max_drawdown:>6.2f}%   "
            f"Avg DD {average_drawdown:>6.2f}%"
        )

print()
print("-" * 60)

overall_max_drawdown = max(
    max(values)
    for values in allocation_drawdowns.values()
    if values
)

print(
    f"Overall maximum NAV drawdown: "
    f"{overall_max_drawdown:>6.2f}%"
)

print(
    f"Maximum allocation: "
    f"{max(allocation_counts.keys()):.0f}%"
)

print(
    f"Trading days analyzed: "
    f"{total_days:,}"
)

print("=" * 60)