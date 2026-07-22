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

        metadata = None

        for name, value in vars(module).items():

            if (
                name.endswith("_METADATA")
                and isinstance(value, dict)
            ):

                metadata = value
                break

        if metadata is None:

            raise ValueError(
                f"No *_METADATA object found in {file.name}"
            )

        objects[
            metadata["slug"]
        ] = metadata

    return objects