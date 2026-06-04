from src.services.price_cache_service import (
    PriceCacheService
)

def get_live_price(
    symbol
):

    try:

        return (
            PriceCacheService
            .get_price(
                symbol
            )
        )

    except Exception as e:

        print(

            f"Price lookup failed "
            f"for {symbol}: {e}"
        )

        return None