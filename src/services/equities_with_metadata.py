import yaml
from pathlib import Path
from app.config.environment import (BASE_DIR)

# Paths

metadata_path = BASE_DIR / "config" / "metadata" / "ticker_metadata.yaml"
output_path = BASE_DIR / "config" / "watchlists" / "equities_with_metadata.yaml"

# Load metadata
metadata = yaml.safe_load(metadata_path.read_text())

# Extract tickers that exist in metadata
valid_tickers = list(metadata.keys())

# Build new tickers.yaml structure
tickers_yaml = {"tickers": sorted(valid_tickers)}

# Save to new file
output_path.write_text(yaml.dump(tickers_yaml, sort_keys=False, indent=2))

print(f"Updated {output_path} with {len(valid_tickers)} tickers from metadata.")
