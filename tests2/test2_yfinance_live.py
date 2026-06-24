import pandas as pd
import yfinance as yf


def test_yfinance_returns_prices():
    ticker = yf.Ticker("MSFT")

    df = ticker.history(period="1mo", interval="1d")

    # Basic checks
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) > 0

    # Required OHLCV columns
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        assert col in df.columns
