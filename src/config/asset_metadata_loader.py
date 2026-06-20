from pathlib import Path
import yaml

from app.config.environment import (
    BASE_DIR
)

import yaml


class AssetMetadataLoader:

    @staticmethod
    def load():
        path = BASE_DIR / "config" / "metadata" / "asset_metadata.yaml"
        with open(path, "r") as file:
            return yaml.safe_load(file)


class TickerLoader:
    @staticmethod
    def load():
        path = BASE_DIR / "config" / "watchlists" / "equities.yaml"
        with open(path, "r") as file:
            return yaml.safe_load(file)

class TickerMetadataLoader:
    @staticmethod
    def load():
        path = BASE_DIR / "config" / "metadata" / "ticker_metadata.yaml"
        with open(path, "r") as file:
            return yaml.safe_load(file)
