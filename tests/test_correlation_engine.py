from src.pipelines.market_pipeline import (
    MarketPipeline
)

from src.services.correlation_service import (
    CorrelationService
)

pipeline = MarketPipeline()

market_context = (
    pipeline.run_watchlist(
        "equities"
    )
)

correlation_matrix = (

    CorrelationService
    .correlation_matrix(

        market_context.get_all()
    )
)

print(
    correlation_matrix.round(2)
)