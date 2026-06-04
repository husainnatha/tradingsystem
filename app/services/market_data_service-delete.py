from pathlib import Path
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

from app.config.environment import (
    DATA_DIR
)

CACHE_DIR = (

    DATA_DIR
    / "cache"
)

CACHE_DIR.mkdir(

    parents=True,

    exist_ok=True
)

CACHE_FILE = (

    CACHE_DIR
    / "market_prices.parquet"
)

# -----------------------------------
# LOAD MARKET PRICES
# -----------------------------------

_cached_market_data = None


def load_market_prices(

    symbols,

    period="6mo"
):

    global _cached_market_data

    # -----------------------------------
    # MEMORY CACHE
    # -----------------------------------

    if _cached_market_data is not None:

        print(

            "\nUsing in-memory prices...\n"
        )

        return _cached_market_data

    # -----------------------------------
    # FILE CACHE
    # -----------------------------------

    if CACHE_FILE.exists():

        modified = datetime.fromtimestamp(

            CACHE_FILE.stat().st_mtime
        )

        age = (

            datetime.now()

            - modified
        )

        if age < timedelta(

            days=1
        ):

            print(

                "\nLoading cached prices...\n"
            )

            _cached_market_data = (

                pd.read_pickle(
                    CACHE_FILE
                )
            )

            return _cached_market_data

    # -----------------------------------
    # DOWNLOAD
    # -----------------------------------

    print(
    "\nRequesting market prices...\n"
)

    data = yf.download(

        symbols,

        period=period,

        group_by="ticker",

        progress=False
    )

    data.to_pickle(

        CACHE_FILE
    )

    _cached_market_data = data

    print(

        "\nMarket cache updated.\n"
    )

    return data