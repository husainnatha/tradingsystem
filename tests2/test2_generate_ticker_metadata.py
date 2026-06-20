import yfinance as yf
import yaml
from pathlib import Path

# Load your existing metadata
metadata_path = Path("config/metadata/ticker_metadata.yaml")
metadata = yaml.safe_load(metadata_path.read_text())

# Load tickers
tickers_path = Path("config/watchlists/equities.yaml")
tickers = yaml.safe_load(tickers_path.read_text())["tickers"]

for ticker in tickers:
    if ticker not in metadata:
        try:
            info = yf.Ticker(ticker).info
            sector = info.get("sector", "UNKNOWN")
            industry = info.get("industry", "UNKNOWN")

            metadata[ticker] = {
                "sector": sector,
                "sub_sector": industry,
                "themes": [],
                "quality": None,
                "conviction": None,
            }
            print(f"Added {ticker} with sector={sector}, sub_sector={industry}")
        except Exception as e:
            print(f"Could not fetch {ticker}: {e}")

# Save back to YAML
metadata_path.write_text(yaml.dump(metadata, sort_keys=True, indent=2))
