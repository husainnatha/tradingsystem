from unittest.mock import patch
import pandas as pd
from src.data.loaders.market_data_loader import MarketDataLoader


@patch("src.data.providers.yfinance_provider.yf.download")
def test_market_data_loader(mock_download):
    # Fake DataFrame
    df_fake = pd.DataFrame({
        "Close": [100, 101, 102],
        "Open": [99, 100, 101],
    })

    mock_download.return_value = df_fake

    loader = MarketDataLoader()
    df = loader.load("NVDA", refresh=True)

    assert len(df) == 3
