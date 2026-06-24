import os
import yaml
from pathlib import Path
from src.services.metadata_enricher import enrich_metadata


def test_metadata_enricher():
    """
    Loads the stock metadata, enriches it, and prints the output
    ONLY when ENV=dev. No files are written.
    """

    # Input metadata file
    input_path = Path("config/metadata/stock_metadata.yaml")
    assert input_path.exists(), f"Missing file: {input_path}"

    # Load raw metadata
    with open(input_path, "r") as f:
        raw = yaml.safe_load(f)

    # Run enrichment
    enriched = enrich_metadata(raw)

    # Print to terminal ONLY in dev mode
    if os.getenv("ENV") == "dev":
        print("\n=== ENRICHED METADATA (DEV MODE) ===")
        print(yaml.dump(enriched, sort_keys=False))

    # Basic structural validation
    assert isinstance(enriched, dict)
    assert len(enriched) > 0

    # Validate one entry
    symbol = next(iter(enriched))
    entry = enriched[symbol]

    required_fields = [
        "asset_type",
        "role",
        "role_category",
        "sector",
        "sub_sector",
        "conviction",
        "quality",
        "innovation_score",
        "market_cap_style",
        "theme_count",
        "themes",
        "inferred_themes",
    ]

    for field in required_fields:
        assert field in entry, f"Missing field: {field}"

    assert isinstance(entry["themes"], list)
    assert isinstance(entry["inferred_themes"], list)
    assert isinstance(entry["innovation_score"], float)
