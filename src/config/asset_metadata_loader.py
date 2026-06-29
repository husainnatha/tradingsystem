from pathlib import Path

import yaml


class AssetMetadataLoader:

    @staticmethod
    def load():

        path = (

            Path("config")

            / "asset_data"

            / "asset_metadata.yaml"
        )

        with open(
            path,
            "r"
        ) as file:

            return yaml.safe_load(file)