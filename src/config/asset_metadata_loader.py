from pathlib import Path
import yaml

from app.config.environment import (
    BASE_DIR
)


class CoreMacroMetadataLoader:
    @staticmethod
    def load():
        path = BASE_DIR / "config" / "metadata" / "core_macro_metadata.yaml"
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
        path = BASE_DIR / "config" / "metadata" / "stock_metadata.yaml"
        with open(path, "r") as file:
            return yaml.safe_load(file)
