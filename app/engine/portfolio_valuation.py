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

    for symbol, data in remaining_pool.items():

        quantity = data[
            "total_quantity"
        ]

        total_cost = data[
            "total_cost"
        ]

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
                round(current_price_gbp, 2),

            "current_price_gbp":
                round(current_price_gbp, 2),
            
            "usd_to_gbp":
                round(current_price_gbp, 2),

            "market_value":
                round(market_value, 2),

            "unrealised_pl":
                round(unrealised_pl, 2)
        })

    return portfolio