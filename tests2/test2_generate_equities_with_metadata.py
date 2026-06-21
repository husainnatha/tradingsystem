import yaml
from pathlib import Path
from app.config.environment import (
    BASE_DIR
)

def test_generate_equities_with_metadata():

    # Paths

    metadata_path = BASE_DIR / "config" / "metadata" / "stock_metadata.yaml"
    output_path = BASE_DIR / "config" / "watchlists" / "equities_with_metadata.yaml"

    metadata = yaml.safe_load(metadata_path.read_text())
    valid_tickers = list(metadata.keys())
    tickers_yaml = {"tickers": sorted(valid_tickers)}

    output_path.write_text(yaml.dump(tickers_yaml, sort_keys=False, indent=2))

    print(f"Updated {output_path} with {len(valid_tickers)} tickers from metadata.")
