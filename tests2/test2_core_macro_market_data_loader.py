from src.data.loaders.market_data_loader import MarketDataLoader

def test_market_data_loader():

    loader = MarketDataLoader()

    df = loader.load(
        ticker="GC=F",
        period="1d"
    )

    print(df.tail())

    assert df is not None
