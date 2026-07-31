import json
from pathlib import Path


def write_json(result: dict, output_file: str) -> None:
    """
    Write a result dictionary to a JSON file.
    """

    output_path = Path(output_file)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            indent=4,
        )

    print(f"JSON written to: {output_path}")