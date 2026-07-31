import json
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"


def build_manifest():

    files = []

    for file in CACHE_DIR.glob("*.json"):

        if file.name == "manifest.json":
            continue

        files.append(file.name)

    manifest = {
        "files": sorted(files)
    }

    with open(CACHE_DIR / "manifest.json", "w") as f:
        json.dump(
            manifest,
            f,
            indent=4,
        )


if __name__ == "__main__":
    build_manifest()
