from src.pipelines.market_pipeline import (
    MarketPipeline
)

from src.services.correlation_service import (
    CorrelationService
)


def test_correlation_service():

    pipeline = MarketPipeline()

    market_context = pipeline.run_watchlist(
        "equities"
    )

    correlation_matrix = (
        CorrelationService
        .correlation_matrix(
            market_context
        )
    )

    print(correlation_matrix.round(2))

    assert True

