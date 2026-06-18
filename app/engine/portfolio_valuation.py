from app.engine.matching_engine import (
    get_section_104_pool
)

from src.services.price_cache_service import (
    PriceCacheService
)

from src.services.fx_service import (
    FXService
)

def get_portfolio_valuation():

    results = get_section_104_pool()

    remaining_pool = results[
        "remaining_pool"
    ]

    portfolio = []

    usd_to_gbp = (
            FXService.get_usd_gbp()
        )

    for symbol, data in remaining_pool.items():

        quantity = data["total_quantity"]

        total_cost = data["total_cost"]

        if quantity <= 0:

            continue

        average_cost = (

            total_cost /

            quantity
        )

        current_price_usd = (

            PriceCacheService
            .get_price(symbol)
        )

        current_price_usd = (

    PriceCacheService
    .get_price(symbol)
    )

    price_available = True

    if current_price_usd is None:

        price_available = False

        current_price_usd = 0

        print(
            f"WARNING: "
            f"No market price for {symbol}"
        )

        usd_to_gbp = (
            FXService.get_usd_gbp()
        )

        current_price_gbp = (
            current_price_usd *
            usd_to_gbp
        )

        market_value = (
            quantity *
            current_price_gbp
        )

        unrealised_pl = (

            market_value -

            total_cost
        )

        portfolio.append({

            "symbol":
                symbol,

            "quantity":
                round(quantity, 2),

            "average_cost":
                round(average_cost, 2),

            "current_price_usd":
                round(current_price_usd, 2),

            "current_price_gbp":
                round(current_price_gbp, 2),

            "usd_to_gbp":
                round(usd_to_gbp, 4),

            "market_value":
                round(market_value, 2),

            "unrealised_pl":
                round(unrealised_pl, 2),

            "price_available":
                round(price_available, 2)
        })

    return portfolio