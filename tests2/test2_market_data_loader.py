from src.data.loaders.market_data_loader import MarketDataLoader


def test_market_data_loader():

    loader = (
        MarketDataLoader()
    )

    df = loader.load(
        ticker="NVDA"
    )

    assert len(df) > 0