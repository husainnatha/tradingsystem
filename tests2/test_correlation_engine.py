from src.pipelines.market_pipeline import (
    MarketPipeline
)

from src.services.correlation_service import (
    CorrelationService
)


pipeline = MarketPipeline()

market_data = pipeline.run_watchlist(
    "core_macro"
)

correlation_matrix = (
    CorrelationService
    .correlation_matrix(
        market_data
    )
)

print(correlation_matrix.round(2))