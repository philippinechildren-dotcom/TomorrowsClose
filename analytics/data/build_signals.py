import json
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"


def build_signals():

    signals = []

    for file in CACHE_DIR.glob("*.json"):

        if file.name in (
            "index.json",
            "rankings.json",
            "signals.json",
            "campaigns.json",
        ):
            continue

        with open(file) as f:
            data = json.load(f)

        if "strategy" not in data:
            continue

        signals.append(
            {
                "strategy": data["strategy"]["name"],
                "ticker": data["strategy"]["ticker"],
                "signal": "COMING SOON",
                "position": "UNKNOWN",
                "trigger_price": None,
            }
        )

    with open(CACHE_DIR / "signals.json", "w") as f:
        json.dump(
            {
                "signals": signals,
            },
            f,
            indent=4,
        )


if __name__ == "__main__":
    build_signals()
