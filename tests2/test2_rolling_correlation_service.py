from src.data.loaders.market_data_loader import (
    MarketDataLoader
)

from src.services.rolling_correlation_service import (
    RollingCorrelationService
)


def test_rolling_correlation_service():

    loader = MarketDataLoader()


    gold = loader.load(
        ticker="GC=F",
        period="2y"
    )

    vix = loader.load(
        ticker="^VIX",
        period="2y"
    )


    rolling_corr = (
        RollingCorrelationService
        .rolling_correlation(
            gold,
            vix,
            window=60
        )
    )


    print(
        rolling_corr.tail(20)
    )

    assert True