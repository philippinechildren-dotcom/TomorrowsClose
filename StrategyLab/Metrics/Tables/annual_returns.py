def build_annual_returns(
    strategy_result,
):
    """
    Build Annual Returns table.

    Calculates annual returns and max EOD drawdown using the exact same
    daily equity curve as metrics.py.
    """
    history = strategy_result.get("history")
    equity_curve = strategy_result.get("equity_curve")
    starting_equity = strategy_result.get("starting_equity", 100000.0)

    if history is None or history.empty or not equity_curve:
        return []

    dates = list(history.index)

    # Handle case where equity_curve has 1 extra initial element (starting equity)
    if len(equity_curve) == len(dates) + 1:
        equity_curve = equity_curve[1:]

    if len(dates) != len(equity_curve):
        return []

    # 1. Track global high-water mark across all time (identical to metrics.py)
    global_max_equity = starting_equity
    
    # Track daily drawdown and group by calendar year
    annual_data = {}

    for date, equity in zip(dates, equity_curve):
        year = date.year

        # High-water mark continuously carried over across year boundaries
        if equity > global_max_equity:
            global_max_equity = equity

        # Drawdown relative to global peak
        drawdown = (equity - global_max_equity) / global_max_equity

        if year not in annual_data:
            annual_data[year] = {
                "end_equity": equity,
                "max_eod_drawdown": 0.0,
            }

        annual_data[year]["end_equity"] = equity

        # Track worst daily drawdown experienced during this year
        if drawdown < annual_data[year]["max_eod_drawdown"]:
            annual_data[year]["max_eod_drawdown"] = drawdown

    # 2. Build final annual returns rows
    annual_returns = []
    years = sorted(annual_data.keys())
    previous_end_equity = starting_equity

    for year in years:
        data = annual_data[year]

        annual_return = (
            data["end_equity"] - previous_end_equity
        ) / previous_end_equity

        annual_returns.append(
            {
                "year": year,
                "return": annual_return,
                "max_eod_drawdown": data["max_eod_drawdown"],
            }
        )

        previous_end_equity = data["end_equity"]

    annual_returns.sort(
        key=lambda row: row["year"],
        reverse=True,
    )

    return annual_returns