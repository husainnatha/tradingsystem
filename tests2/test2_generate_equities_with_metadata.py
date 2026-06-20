import yaml
from pathlib import Path

def test_generate_equities_with_metadata():
    metadata_path = Path(r"C:\Users\husainnatha\projects\tradingsystem\config\metadata\ticker_metadata.yaml")
    output_path = Path(r"C:\Users\husainnatha\projects\tradingsystem\config\watchlists\equities_with_metadata.yaml")

    metadata = yaml.safe_load(metadata_path.read_text())
    valid_tickers = list(metadata.keys())
    tickers_yaml = {"tickers": sorted(valid_tickers)}

    output_path.write_text(yaml.dump(tickers_yaml, sort_keys=False, indent=2))

    print(f"Updated {output_path} with {len(valid_tickers)} tickers from metadata.")
