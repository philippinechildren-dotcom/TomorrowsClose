from dataclasses import dataclass


@dataclass
class Trade:
    """
    One completed trade.
    """

    # ==========================================================
    # Entry
    # ==========================================================

    entry_date: object
    entry_price: float
    entry_equity: float

    # ==========================================================
    # Exit
    # ==========================================================

    exit_date: object
    exit_price: float

    # ==========================================================
    # Position
    # ==========================================================

    shares: float

    # ==========================================================
    # Results
    # ==========================================================

    pnl: float
    return_pct: float
    days_held: int

    winning_trade: bool
    strategy_number: int = 0


def build_trades(
    signals,
    starting_equity=100000.0,
):
    """
    Convert BUY/SELL signals into completed trades.

    Parameters
    ----------
    signals
        List of BUY / SELL signals.

    starting_equity
        Initial account value.

    Returns
    -------
    dict

        {
            "trades": [...],
            "closed_equity": [...]
        }
    """

    trades = []

    closed_equity = []

    current_equity = starting_equity

    position = None

    # ==========================================================
    # Process Signals
    # ==========================================================

    for signal in signals:

        action = signal["signal"]

        price = float(
            signal["price"]
        )

        date = signal["date"]

        # ------------------------------------------------------
        # BUY
        # ------------------------------------------------------

        if (
            action == "BUY"
            and position is None
        ):

            shares = (
                current_equity
                /
                price
            )

            position = {

                "entry_date": date,

                "entry_price": price,

                "entry_equity": current_equity,

                "shares": shares,

                "strategy_number": signal.get(
                    "strategy_number",
                    0,
                ),

            }

            continue

        # ------------------------------------------------------
        # SELL
        # ------------------------------------------------------

        if (
            action == "SELL"
            and position is not None
        ):

            pnl = (

                price
                -
                position["entry_price"]

            ) * position["shares"]

            current_equity += pnl

            closed_equity.append(
                current_equity
            )

            return_pct = (

                price
                /
                position["entry_price"]

            ) - 1

            days_held = (

                date
                -
                position["entry_date"]

            ).days

            trades.append(

                Trade(

                    entry_date=position["entry_date"],

                    entry_price=position["entry_price"],

                    entry_equity=position["entry_equity"],

                    exit_date=date,

                    exit_price=price,

                    shares=position["shares"],

                    pnl=pnl,

                    return_pct=return_pct,

                    days_held=days_held,

                    winning_trade=pnl > 0,

                    strategy_number=position[
                        "strategy_number"
                    ],

                )

            )

            position = None

    return {
        "trades": trades,
        "closed_equity": closed_equity,
    }