from src.pipelines.market_pipeline import (
    MarketPipeline
)


pipeline = MarketPipeline()

results = pipeline.run_watchlist(
    "core_macro"
)


for ticker, df in results.items():

    print(f"\n{ticker}")

    print(
        df[
            [
                "Close",
                "MA50",
                "MA200",
                "RSI"
            ]
        ].tail(2)
    )

# from src.services.market_data_service import (
#     MarketDataService
# )

# from src.data.loaders.watchlist_loader import (
#     WatchlistLoader
# )


# watchlist = WatchlistLoader.load(
#     "core_macro"
# )

# service = MarketDataService()


# for ticker in watchlist:

#     print(f"\nProcessing: {ticker}")

#     df = service.build_processed_dataset(
#         ticker=ticker
#     )

#     print(
#         df[
#             [
#                 "Close",
#                 "MA50",
#                 "MA200",
#                 "RSI"
#             ]
#         ].tail(2)
#     )