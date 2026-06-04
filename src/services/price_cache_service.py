from datetime import UTC
from datetime import datetime

import yfinance as yf


class PriceCacheService:

    _cache = {}

    @classmethod
    def refresh_price(
        cls,
        symbol
    ):

        ticker = yf.Ticker(
            symbol
        )

        history = ticker.history(
            period="1d"
        )

        if history.empty:

            return None

        price = float(

            history.iloc[-1][
                "Close"
            ]
        )

        cls._cache[
            symbol
        ] = {

            "price":
                price,

            "updated":

                datetime.now(
                    UTC
                ).isoformat()
        }

        return price

    @classmethod
    def get_price(
        cls,
        symbol
    ):

        if symbol not in cls._cache:

            return cls.refresh_price(
                symbol
            )

        return cls._cache[
            symbol
        ][
            "price"
        ]