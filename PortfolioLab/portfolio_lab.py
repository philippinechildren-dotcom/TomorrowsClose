import pandas as pd
import numpy as np
from StrategyLab.Strategies.rsi_threshold import build_result as build_rsi
from StrategyLab.Strategies.lowhigh import build_result as build_lowhigh
from StrategyLab.Strategies.turnaround_tuesday import build_result as build_tt
from StrategyLab.Strategies.ulcershield import build_result as build_ulcershield
from StrategyLab.Strategies.lowhigh_ulcershield import build_result as build_lowhigh_ulcershield


def build_buy_and_hold(ticker="QQQ", period="maximum", starting_equity=100000.0):
    from StrategyLab.Strategies.lowhigh import get_market_history, filter_history
    history = get_market_history(ticker=ticker)
    history = filter_history(history, period)
    
    closes = history["close"].astype(float)
    returns = closes.pct_change().fillna(0.0)
    equity_curve = (1 + returns).cumprod() * starting_equity
    
    return {
        "name": "Buy and Hold",
        "equity_curve": equity_curve.tolist(),
        "dates": history.index.astype(str).tolist()
    }


STRATEGY_MAP = {
    "buy_and_hold": build_buy_and_hold,
    "rsi_threshold": build_rsi,
    "lowhigh": build_lowhigh,
    "turnaround_tuesday": build_tt,
    "ulcershield": build_ulcershield,
    "lowhigh_ulcershield": build_lowhigh_ulcershield,
}


def build_portfolio_result(legs, rebalance_schedule="no_rebalance", period="maximum", starting_equity=100000.0):
    """
    legs: list of dicts -> [{'strategy': 'lowhigh', 'etf': 'QQQ', 'allocation': 25}, ...]
    rebalance_schedule: 'no_rebalance', '3_months', '6_months', '1_year'
    """
    valid_legs = []
    
    for leg in legs:
        strat_key = leg.get("strategy")
        etf = leg.get("etf", "QQQ")
        alloc = float(leg.get("allocation", 0.0)) / 100.0
        
        if strat_key in STRATEGY_MAP and alloc > 0:
            valid_legs.append({
                "strategy": strat_key,
                "etf": etf,
                "target_allocation": alloc
            })

    if not valid_legs:
        return {}

    # Extract equity curves as proper time-indexed series
    series_dict = {}
    target_weights = []

    for i, leg in enumerate(valid_legs):
        builder = STRATEGY_MAP[leg["strategy"]]
        res = builder(ticker=leg["etf"], period=period, starting_equity=starting_equity)
        
        # Safely extract dates from 'history' dataframe index or dictionary keys
        if "history" in res and hasattr(res["history"], "index"):
            raw_dates = res["history"].index
        else:
            raw_dates = res.get("dates") or res.get("dates_index") or []
        
        # Convert dates directly into datetime objects
        leg_dates = pd.to_datetime(raw_dates, utc=True).tz_localize(None)
        eq_curve = res.get("equity_curve", [])

        # Guard length alignment
        if len(eq_curve) > len(leg_dates):
            eq_curve = eq_curve[-len(leg_dates):]
        elif len(leg_dates) > len(eq_curve):
            leg_dates = leg_dates[-len(eq_curve):]

        # Map series to dates
        eq_series = pd.Series(eq_curve, index=leg_dates)
        
        # Store daily percentage returns
        series_dict[f"leg_{i}"] = eq_series.pct_change().fillna(0.0)
        target_weights.append(leg["target_allocation"])

    # Combine into unified DataFrame & align to the most restrictive common start date
    returns_df = pd.DataFrame(series_dict).dropna()
    target_weights = np.array(target_weights)
    
    if returns_df.empty:
        return {}

    # Normalize weights if total doesn't equal 100%
    if target_weights.sum() > 0:
        target_weights = target_weights / target_weights.sum()

    n_days, n_legs = returns_df.shape
    portfolio_equity = np.zeros(n_days)
    portfolio_equity[0] = starting_equity
    
    current_leg_values = starting_equity * target_weights

    for i in range(1, n_days):
        current_date = returns_df.index[i]
        prev_date = returns_df.index[i - 1]
        
        # Apply daily market returns to current value
        day_rets = returns_df.iloc[i].values
        current_leg_values = current_leg_values * (1.0 + day_rets)
        total_val = current_leg_values.sum()
        
        # Check rebalance condition
        should_rebalance = False
        if rebalance_schedule == "3_months":
            should_rebalance = (current_date.month != prev_date.month) and (current_date.month in [1, 4, 7, 10])
        elif rebalance_schedule == "6_months":
            should_rebalance = (current_date.month != prev_date.month) and (current_date.month in [1, 7])
        elif rebalance_schedule == "1_year":
            should_rebalance = (current_date.year != prev_date.year)

        if should_rebalance:
            current_leg_values = total_val * target_weights

        portfolio_equity[i] = total_val

    combined_curve = pd.Series(portfolio_equity, index=returns_df.index)

    # Risk and Return Metrics
    cum_max = combined_curve.cummax()
    drawdown = (combined_curve - cum_max) / cum_max
    max_eod_dd = float(drawdown.min())
    
    dates_index = returns_df.index
    years = (dates_index[-1] - dates_index[0]).days / 365.25 if len(dates_index) > 1 else 0.0
    
    cagr = float((combined_curve.iloc[-1] / starting_equity) ** (1 / years) - 1) if years > 0 and combined_curve.iloc[-1] > 0 else 0.0
    ulcer_index = float(np.sqrt(np.mean(drawdown ** 2)) * 100)
    upi = float((cagr * 100) / ulcer_index) if ulcer_index > 0 else 0.0

    return {
        "metrics": {
            "cagr": float(cagr),
            "max_eod_drawdown": float(max_eod_dd),
            "ulcer_index": float(ulcer_index),
            "ulcer_performance_index": float(upi),
        },
        "equity_curve": combined_curve.tolist(),
        "dates": returns_df.index.astype(str).tolist(),
    }