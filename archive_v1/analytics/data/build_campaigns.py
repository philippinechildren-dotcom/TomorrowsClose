import json
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"


def build_campaigns():

    campaigns = []

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

        if "performance" not in data:
            continue

        performance = data["performance"]

        campaigns.append(
            {
                "strategy": data["strategy"]["name"],
                "ticker": data["strategy"]["ticker"],
                "campaign_count": performance.get(
                    "campaign_count",
                    0,
                ),
                "max_closed_drawdown": performance.get(
                    "max_closed_drawdown",
                    0,
                ),
            }
        )

    with open(CACHE_DIR / "campaigns.json", "w") as f:
        json.dump(
            {
                "campaigns": campaigns,
            },
            f,
            indent=4,
        )


if __name__ == "__main__":
    build_campaigns()
