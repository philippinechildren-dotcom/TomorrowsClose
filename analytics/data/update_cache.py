import json
from pathlib import Path
from datetime import datetime, UTC

from analytics.data.market_status import latest_market_date

from analytics.data.build_rankings import build_rankings
from analytics.data.build_signals import build_signals
from analytics.data.build_campaigns import build_campaigns
from analytics.data.build_trade_log import build_trade_log
from analytics.data.build_manifest import build_manifest
from analytics.data.cache_status import build_status
from analytics.strategies.build_buy_and_hold import build_buy_and_hold
from analytics.strategies.build_lowhigh import build_lowhigh
from analytics.strategies.build_rsi_pricesolver import build_rsi_pricesolver
from analytics.strategies.build_ulcershield import build_ulcershield

from analytics.strategies.performance import build_performance_report


CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)


def write_strategy_file(
    strategy_name: str,
    ticker: str,
    result: dict,
):

    report = build_performance_report(
        starting_equity=result["starting_equity"],
        ending_equity=result["ending_equity"],
        equity_curve=result["equity_curve"],
        start_date=result["start_date"],
        end_date=result["end_date"],
        trades=result.get("trades"),
    )

    filename = (
        strategy_name.lower()
        .replace(" ", "_")
        .replace("&", "and")
        + "_"
        + ticker.lower()
        + ".json"
    )

    data = {
        "strategy": {
            "name": strategy_name,
            "ticker": ticker,
            "category": (
                "Benchmark"
                if strategy_name == "Buy & Hold"
                else "EasyMode"
            ),
        },
        "performance": report,
    }

    with open(CACHE_DIR / filename, "w") as f:
        json.dump(
            data,
            f,
            indent=4,
            default=str,
        )

    return {
        "name": strategy_name,
        "ticker": ticker,
        "file": filename,
    }


def update_cache():

    strategies = []

    strategies.append(
        write_strategy_file(
            "Buy & Hold",
            "QQQ",
            build_buy_and_hold(
                ticker="QQQ",
            ),
        )
    )

    strategies.append(
        write_strategy_file(
            "LowHigh",
            "QLD",
            build_lowhigh(
                ticker="QLD",
            ),
        )
    )

    strategies.append(
        write_strategy_file(
            "RSI PriceSolver",
            "QQQ",
            build_rsi_pricesolver(
                ticker="QQQ",
            ),
        )
    )

    strategies.append(
        write_strategy_file(
            "UlcerShield",
            "QQQ",
            build_ulcershield(
                ticker="QQQ",
            ),
        )
    )

    index = {
        "last_updated": datetime.now(UTC).isoformat(),
        **build_status(latest_market_date()),
        "strategy_count": len(strategies),
        "strategies": strategies,
    }

    with open(CACHE_DIR / "index.json", "w") as f:
        json.dump(
            index,
            f,
            indent=4,
        )

    # Build rankings AFTER all strategy files exist
    build_rankings()
    build_signals()
    build_campaigns()
    build_trade_log()
    build_manifest()

if __name__ == "__main__":
    update_cache()