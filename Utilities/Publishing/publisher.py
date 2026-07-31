import json
from pathlib import Path

from EasyMode.RSI_PriceSolver.price_solver import build_result


OUTPUT_DIRECTORY = Path("output/json")


def write_json(data, filename):
    filename.parent.mkdir(parents=True, exist_ok=True)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"JSON written to: {filename}")


def build_homepage():

    return build_result(
        ticker="QQQ",
        rsi_period=3,
        threshold=30,
        dataset="VISITOR",
    )


def build_free():

    return build_result(
        ticker="QQQ",
        rsi_period=3,
        threshold=30,
        dataset="FREE",
    )

def build_paid():

    return build_result(
        ticker="QQQ",
        rsi_period=3,
        threshold=30,
        dataset="PAID",
    )

def build_homepage_json():

    homepage = build_homepage()

    write_json(
        homepage,
        OUTPUT_DIRECTORY / "homepage" / "rsi_pricesolver.json",
    )