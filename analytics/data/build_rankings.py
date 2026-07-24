import json
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"


def build_rankings():

    rankings = []

    for file in CACHE_DIR.glob("*.json"):

        if file.name in (
            "index.json",
            "rankings.json",
            "signals.json",
        ):
            continue

        with open(file) as f:
            data = json.load(f)

        if "performance" not in data:
            continue

        performance = data["performance"]

        rankings.append(
            {
                "strategy": data["strategy"]["name"],
                "ticker": data["strategy"]["ticker"],
                "category": data["strategy"]["category"],
                "cagr": performance["cagr"],
                "upi": performance["upi"],
                "max_eod_drawdown": performance["max_eod_drawdown"],
                "max_closed_drawdown": performance["max_closed_drawdown"],
            }
        )

    rankings.sort(
        key=lambda x: x["upi"],
        reverse=True,
    )

    for rank, row in enumerate(rankings, start=1):
        row["rank"] = rank

    with open(CACHE_DIR / "rankings.json", "w") as f:
        json.dump(
            {
                "rankings": rankings,
            },
            f,
            indent=4,
        )


if __name__ == "__main__":
    build_rankings()
