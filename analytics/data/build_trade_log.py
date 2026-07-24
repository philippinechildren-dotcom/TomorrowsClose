import json
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"


def build_trade_log():

    trades = []

    for file in CACHE_DIR.glob("*.json"):

        if file.name in (
            "index.json",
            "rankings.json",
            "signals.json",
            "campaigns.json",
            "trade_log.json",
        ):
            continue

        with open(file) as f:
            data = json.load(f)

        if "strategy" not in data:
            continue

        if "trades" not in data["performance"]:
            continue

        for trade in data["performance"]["trades"]:

            trades.append(
                {
                    "strategy": data["strategy"]["name"],
                    "ticker": data["strategy"]["ticker"],
                    "trade": trade,
                }
            )

    with open(CACHE_DIR / "trade_log.json", "w") as f:
        json.dump(
            {
                "trades": trades,
            },
            f,
            indent=4,
        )


if __name__ == "__main__":
    build_trade_log()
