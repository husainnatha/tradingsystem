import yaml
from app.engine.scoring_engine import compute_scores

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def write_yaml(path, data):
    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=True)

def generate_metadata():
    equities = load_yaml("config/metadata/stock_metadata.yaml")

    metadata = {}

    # Process STOCKS only
    for ticker, entry in equities.items():
        entry["asset_type"] = "STOCK"

        conviction, quality, role = compute_scores(ticker, entry)

        entry["conviction"] = conviction
        entry["quality"] = quality
        entry["role"] = role

        metadata[ticker] = entry

    # Write a FLAT dictionary (no stock_metadata wrapper)
    write_yaml("config/metadata/asset_metadata.yaml", metadata)
    print("Generated config/metadata/asset_metadata.yaml")

if __name__ == "__main__":
    generate_metadata()
