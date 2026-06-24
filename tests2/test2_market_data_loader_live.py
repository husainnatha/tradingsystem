from unittest.mock import patch
import pandas as pd
from src.data.loaders.market_data_loader import MarketDataLoader


def test_market_data_loader():
    
        loader = (
            MarketDataLoader()
        )
    
        df = loader.load(
            ticker="MSFT"
        )

        assert len(df) > 0
