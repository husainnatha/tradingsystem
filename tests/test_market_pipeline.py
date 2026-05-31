from src.pipelines.market_pipeline import (
    MarketPipeline
)


pipeline = MarketPipeline()

results = pipeline.run_watchlist(
    "equities"
)


for ticker, df in (
    results.get_all().items()
):
    print(f"\n{ticker}")

    print(
        df[
            [
                "Close",
                "MA50",
                "RSI"
            ]
        ].tail(2)
    )