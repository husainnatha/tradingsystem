import argparse
import yaml
from pathlib import Path

from app.engine.scoring_engine import compute_conviction_and_quality


def run_scoring_service(input_file: str, output_file: str):
    #input_file = "config/asset_data/stock_metadata.yaml" 
    #output_file = "config/asset_data/stock_metadata_processed.yaml"
    input_path = Path(input_file)
    output_path = Path(output_file)

    with open(input_path, "r") as f:
        data = yaml.safe_load(f)

    enriched = {}

    for ticker, entry in data.items():

        # Only score STOCKS
        if entry.get("asset_type") != "STOCK":
            enriched[ticker] = entry
            continue

        conviction, quality, role = compute_conviction_and_quality(ticker, entry)

        entry["conviction"] = conviction
        entry["quality"] = quality
        entry["role"] = role

        # Remove role_category if present
        entry.pop("role_category", None)

        enriched[ticker] = entry

    with open(output_path, "w") as f:
        yaml.dump(enriched, f, sort_keys=False)

    print(f"[scoring_service] Completed. Output written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Run scoring engine service.")
    parser.add_argument("input", help="Path to input YAML metadata file")
    parser.add_argument("output", help="Path to output YAML file")

    args = parser.parse_args()
    run_scoring_service(args.input, args.output)


if __name__ == "__main__":
    main()
