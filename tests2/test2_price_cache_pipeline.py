from src.pipelines.price_cache_pipeline import (
    PriceCachePipeline
)

from src.services.price_cache_service import (
    PriceCacheService
)


def test_price_cache_pipeline():

    PriceCachePipeline().run()

    price = (

        PriceCacheService
        .get_price(
            "NVDA"
        )
    )

    print()

    print(
        f"NVDA: {price}"
    )

    assert price > 0