import json

from pathlib import Path
from datetime import datetime


class MetadataRegistry:

    METADATA_DIR = Path(
        "cache/metadata"
    )

    @classmethod
    def get_metadata_path(
        cls,
        ticker: str,
        interval: str
    ):

        safe_ticker = ticker.replace("^", "_")

        return (
            cls.METADATA_DIR /
            f"{safe_ticker}_{interval}.json"
        )

    @classmethod
    def save_metadata(
        cls,
        ticker: str,
        interval: str,
        rows: int,
        source: str = "yfinance"
    ):

        cls.METADATA_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        path = cls.get_metadata_path(
            ticker,
            interval
        )

        metadata = {

            "ticker": ticker,
            "interval": interval,
            "source": source,
            "rows": rows,
            "last_updated":
                datetime.utcnow().isoformat()
        }

        with open(path, "w") as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

    @classmethod
    def load_metadata(
        cls,
        ticker: str,
        interval: str
    ):

        path = cls.get_metadata_path(
            ticker,
            interval
        )

        if not path.exists():

            return None

        with open(path, "r") as file:

            return json.load(file)