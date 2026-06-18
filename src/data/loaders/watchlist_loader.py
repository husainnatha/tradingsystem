from pathlib import Path
import yaml

from app.config.environment import (
    BASE_DIR
)


class WatchlistLoader:

    WATCHLIST_DIR = Path(
        BASE_DIR
        / "config"
        / "watchlists"
    )

    @classmethod
    def load(
        cls,
        watchlist_name: str
    ):

        path = (
            cls.WATCHLIST_DIR /
            f"{watchlist_name}.yaml"
        )

        if not path.exists():

            raise FileNotFoundError(
                f"Watchlist not found: {path}"
            )

        with open(path, "r") as file:

            data = yaml.safe_load(file)

        return data["tickers"]