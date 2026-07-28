def generate_signals(
    full_history,
    entry_lookback: int,
    exit_lookback: int,
):
    signals = []

    position = False

    warmup = max(
        entry_lookback,
        exit_lookback,
    )

    for i in range(warmup, len(full_history)):

        date = full_history.index[i]

        close = float(
            full_history["close"].iloc[i]
        )

        previous_low = full_history["low"].iloc[
            i - entry_lookback:i
        ].min()

        previous_high = full_history["high"].iloc[
            i - exit_lookback:i
        ].max()

        if not position:

            if close < previous_low:

                signals.append({
                    "date": date,
                    "signal": "BUY",
                    "price": close,
                })

                position = True

        else:

            if close > previous_high:

                signals.append({
                    "date": date,
                    "signal": "SELL",
                    "price": close,
                })

                position = False

    return signals