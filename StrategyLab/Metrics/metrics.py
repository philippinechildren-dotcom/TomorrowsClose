from math import inf


def build_metrics(
    equity_curve,
    trades,
    starting_equity,
    ending_equity,
    years,
    exposure,
):
    """
    Build the complete Strategy Lab metrics catalog.
    """

    # ==========================================================
    # Performance
    # ==========================================================

    total_return = (
        ending_equity - starting_equity
    ) / starting_equity

    cagr = (
        (ending_equity / starting_equity) ** (1 / years)
        - 1
    ) if years > 0 else 0.0

    # ==========================================================
    # Trading
    # ==========================================================

    number_of_trades = len(trades)

    trades_per_year = (
        number_of_trades / years
    ) if years > 0 else 0.0

    # ==========================================================
    # Risk
    # ==========================================================

    if equity_curve:
        # Initialize high-water mark safely based on the first data point or starting capital
        max_equity = max(starting_equity, equity_curve[0])
    else:
        max_equity = starting_equity

    max_eod_drawdown = 0.0
    ulcer_sum = 0.0

    for equity in equity_curve:
        # Update high-water mark continuously
        if equity > max_equity:
            max_equity = equity

        # Calculate drawdown relative to highest peak seen so far (guarded against division by zero)
        drawdown = (equity - max_equity) / max_equity if max_equity > 0 else 0.0

        # Track the maximum drawdown (most negative value)
        if drawdown < max_eod_drawdown:
            max_eod_drawdown = drawdown

        # Accumulate squared drawdowns for Ulcer Index calculation
        ulcer_sum += drawdown ** 2

    ulcer_index = (
        (
            ulcer_sum / len(equity_curve)
        ) ** 0.5 * 100
    ) if equity_curve else 0.0

    ulcer_performance_index = (
        (cagr * 100) / ulcer_index
    ) if ulcer_index > 0 else None

    calmar_ratio = (
        cagr / abs(max_eod_drawdown)
    ) if max_eod_drawdown < 0 else inf

        # ==========================================================
    # Maximum Closed Trade Drawdown
    # ==========================================================

    closed_equity = starting_equity
    peak_closed_equity = starting_equity

    max_closed_trade_drawdown = 0.0

    for trade in trades:

        closed_equity += trade.pnl

        if closed_equity > peak_closed_equity:
            peak_closed_equity = closed_equity

        drawdown = (
            closed_equity - peak_closed_equity
        ) / peak_closed_equity

        if drawdown < max_closed_trade_drawdown:
            max_closed_trade_drawdown = drawdown

    # ==========================================================
    # Trade Statistics (Tranche-Aware)
    # ==========================================================

    winners = [trade for trade in trades if trade.winning_trade]
    losers = [trade for trade in trades if not trade.winning_trade]

    win_rate = (
        len(winners) / number_of_trades
    ) if number_of_trades > 0 else 0.0

    # Helper function: Check if trade object specifies position size / tranche weight.
    # If trade has `position_pct` or `weight` (e.g. 0.20), scale return_pct.
    def get_portfolio_trade_return(trade):
        weight = getattr(trade, "weight", getattr(trade, "position_pct", 1.0))
        return trade.return_pct * weight

    average_trade_percent = (
        sum(get_portfolio_trade_return(trade) for trade in trades)
        / number_of_trades
    ) if number_of_trades > 0 else 0.0

    average_win_percent = (
        sum(get_portfolio_trade_return(trade) for trade in winners)
        / len(winners)
    ) if winners else 0.0

    average_loss_percent = (
        sum(get_portfolio_trade_return(trade) for trade in losers)
        / len(losers)
    ) if losers else 0.0

    total_wins = sum(
        get_portfolio_trade_return(trade)
        for trade in winners
    )

    total_losses = sum(
        abs(get_portfolio_trade_return(trade))
        for trade in losers
    )

    profit_factor = (
        total_wins / total_losses
    ) if total_losses > 0 else None

    expectancy_percent = average_trade_percent

    if profit_factor is not None and profit_factor > 0:
        kelly_criterion = win_rate - ((1 - win_rate) / profit_factor)
    elif win_rate == 1.0:
        kelly_criterion = 1.0
    else:
        kelly_criterion = 0.0

    average_hold_days = (
        sum(trade.days_held for trade in trades)
        / number_of_trades
    ) if number_of_trades > 0 else 0.0

    maximum_consecutive_wins = 0
    maximum_consecutive_losses = 0

    win_streaks = []
    loss_streaks = []

    current_win_streak = 0
    current_loss_streak = 0

    for trade in trades:

        if trade.winning_trade:

            current_win_streak += 1

            if current_loss_streak > 0:
                loss_streaks.append(current_loss_streak)
                current_loss_streak = 0

            if current_win_streak > maximum_consecutive_wins:
                maximum_consecutive_wins = current_win_streak

        else:

            current_loss_streak += 1

            if current_win_streak > 0:
                win_streaks.append(current_win_streak)
                current_win_streak = 0

            if current_loss_streak > maximum_consecutive_losses:
                maximum_consecutive_losses = current_loss_streak

    if current_win_streak > 0:
        win_streaks.append(current_win_streak)

    if current_loss_streak > 0:
        loss_streaks.append(current_loss_streak)

    average_consecutive_wins = (
        sum(win_streaks) / len(win_streaks)
    ) if win_streaks else 0.0

    average_consecutive_losses = (
        sum(loss_streaks) / len(loss_streaks)
    ) if loss_streaks else 0.0

    # ==========================================================
    # Metrics Catalog
    # ==========================================================

    return {

        # Performance

        "starting_equity": starting_equity,
        "ending_equity": ending_equity,
        "total_return": total_return,
        "cagr": cagr,

        # Risk

        "max_eod_drawdown": max_eod_drawdown,
        "max_closed_trade_drawdown": max_closed_trade_drawdown,
        "ulcer_index": ulcer_index,
        "ulcer_performance_index": ulcer_performance_index,
        "calmar_ratio": calmar_ratio,

        # Trading

        "number_of_trades": number_of_trades,
        "trades_per_year": trades_per_year,
        "exposure": exposure,
        "win_rate": win_rate,
        "average_trade_percent": average_trade_percent,
        "average_win_percent": average_win_percent,
        "average_loss_percent": average_loss_percent,
        "profit_factor": profit_factor,
        "expectancy_percent": expectancy_percent,
        "kelly_criterion": kelly_criterion,
        "average_hold_days": average_hold_days,
        "maximum_consecutive_wins": maximum_consecutive_wins,
        "maximum_consecutive_losses": maximum_consecutive_losses,
        "average_consecutive_wins": average_consecutive_wins,
        "average_consecutive_losses": average_consecutive_losses,
    }