from importlib import import_module
from pathlib import Path


def load_metadata(folder):

    objects = {}

    metadata_folder = (
        Path(__file__).parent.parent
        / "metadata"
        / folder
    )

    for file in metadata_folder.glob("*.py"):

        if file.stem == "__init__":
            continue

        module = import_module(
            f"metadata.{folder}.{file.stem}"
        )

        metadata = module.METADATA

        objects[
            metadata["slug"]
        ] = metadata

    return objects