from dataclasses import dataclass


@dataclass
class Trade:
    """
    Individual completed trade.
    """

    entry_date: object
    exit_date: object

    entry_price: float
    exit_price: float

    shares: float

    pnl: float
    return_pct: float

    days_held: int

    winning_trade: bool



def build_trades(
    signals,
    starting_equity: float = 100000.0,
) -> list:
    """
    Build individual trades from entry/exit signals.

    Uses TradingView-style compounding:
    100% of current equity invested on each entry.
    """

    trades = []

    position = None

    current_equity = starting_equity


    for signal in signals:

        action = signal["signal"]

        price = float(
            signal["price"]
        )

        date = signal["date"]


        if action == "BUY" and position is None:

            shares = (
                current_equity / price
            )

            position = {

                "entry_date": date,

                "entry_price": price,

                "shares": shares,

                "starting_equity": current_equity,

            }


        elif action == "SELL" and position is not None:

            pnl = (
                (price - position["entry_price"])
                *
                position["shares"]
            )


            current_equity += pnl


            return_pct = (

                price / position["entry_price"]

                - 1

            )


            days_held = (

                date - position["entry_date"]

            ).days


            trades.append(

                Trade(

                    entry_date=position["entry_date"],

                    exit_date=date,

                    entry_price=position["entry_price"],

                    exit_price=price,

                    shares=position["shares"],

                    pnl=pnl,

                    return_pct=return_pct,

                    days_held=days_held,

                    winning_trade=pnl > 0,

                )

            )


            position = None


    return trades