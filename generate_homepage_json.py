from EasyMode.RSI_PriceSolver.price_solver import build_result
from Utilities.publishing.json_writer import write_json


def main():

    result = build_result(
        dataset="homepage_free",
    )

    write_json(
        result=result,
        output_file="output/json/homepage/rsi_pricesolver.json",
    )


if __name__ == "__main__":
    main()