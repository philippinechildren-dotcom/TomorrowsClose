"""
TradingJournal/journal_engine.py
Aggregates executions across production strategy systems using clean, 
standardized labeling (Buy Entry / Sell Exit), computes normalized 
individual trade P&L returns, and caps history to 2 years.
"""
from datetime import datetime, timedelta

from StrategyLab.Strategies.ulcershield import (
    build_result as build_rsi_ulcershield_result,
)
from StrategyLab.Strategies.lowhigh_ulcershield import (
    build_result as build_lowhigh_ulcershield_result,
)
from StrategyLab.Strategies.lowhigh import (
    build_result as build_lowhigh_result,
)
from StrategyLab.Strategies.turnaround_tuesday import (
    build_result as build_tt_result,
)
from StrategyLab.Strategies.rsi_threshold import (
    build_result as build_rsi_threshold_result,
)

DEFAULT_SYSTEMS = [
    {
        "name": "RSI UlcerShield",
        "ticker": "TQQQ",
        "max_tranches": 5,
        "runner": lambda: build_rsi_ulcershield_result(ticker="TQQQ"),
    },
    {
        "name": "LowHigh UlcerShield",
        "ticker": "QLD",
        "max_tranches": 5,
        "runner": lambda: build_lowhigh_ulcershield_result(ticker="QLD"),
    },
    {
        "name": "LowHigh",
        "ticker": "QLD",
        "max_tranches": 1,
        "runner": lambda: build_lowhigh_result(ticker="QLD"),
    },
    {
        "name": "Turnaround Tuesday",
        "ticker": "QQQ",
        "max_tranches": 1,
        "runner": lambda: build_tt_result(ticker="QQQ"),
    },
    {
        "name": "RSI Threshold",
        "ticker": "TQQQ",
        "max_tranches": 1,
        "runner": lambda: build_rsi_threshold_result(ticker="TQQQ"),
    },
]

def process_system_trades(system_info):
    strategy_name = system_info["name"]
    ticker = system_info["ticker"]
    max_tranches = system_info["max_tranches"]
    
    try:
        result = system_info["runner"]()
    except Exception as e:
        print(f"Error executing {strategy_name}: {e}")
        raise

    trades = result.get("trades", [])
    if not trades:
        return []

    journal_rows = []
    sorted_trades = sorted(trades, key=lambda x: x.entry_date)
    
    # 2-Year cutoff (~730 days)
    two_years_ago = datetime.now() - timedelta(days=730)

    for trade in sorted_trades:
        # Align timezone awareness
        if hasattr(trade.entry_date, 'tzinfo') and trade.entry_date.tzinfo is not None:
            if two_years_ago.tzinfo is None:
                two_years_ago = two_years_ago.replace(tzinfo=trade.entry_date.tzinfo)

        # Record BUY entry row
        if trade.entry_date >= two_years_ago:
            journal_rows.append({
                "date": trade.entry_date.strftime("%Y-%m-%d"),
                "strategy": strategy_name,
                "etf": ticker,
                "action": "Buy Entry",
                "price": f"${trade.entry_price:.2f}",
                "pnl": "—"
            })

        # Record SELL exit row
        if trade.exit_date is not None:
            raw_return_pct = trade.return_pct * 100.0
            normalized_pnl = raw_return_pct / max_tranches

            if trade.exit_date >= two_years_ago:
                journal_rows.append({
                    "date": trade.exit_date.strftime("%Y-%m-%d"),
                    "strategy": strategy_name,
                    "etf": ticker,
                    "action": "Sell Exit",
                    "price": f"${trade.exit_price:.2f}",
                    "pnl": f"{normalized_pnl:+.2f}%"
                })

    return journal_rows


def build_master_journal():
    master_logs = []
    for sys in DEFAULT_SYSTEMS:
        logs = process_system_trades(sys)
        master_logs.extend(logs)

    master_logs.sort(key=lambda x: x["date"], reverse=True)
    return master_logs