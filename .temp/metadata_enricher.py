import yaml
from app.config.environment import BASE_DIR

# ----------------------------------------
# 1. Updated Theme Universe
# ----------------------------------------

THEMES = [
    "AI", "PHOTONICS", "SEMICONDUCTORS", "NETWORKING", "DATA_CENTRES",
    "CYBERSECURITY", "QUANTUM", "AUTONOMY", "ROBOTICS", "HEALTHCARE",
    "ENERGY", "FINTECH", "CLOUD", "AUTOMATION", "CONSUMER", "DEFENSIVE",
    "STREAMING", "ENTERTAINMENT", "INNOVATION", "MARKET", "MEMORY"
]

# ----------------------------------------
# 2. Main Enrichment Logic (Non‑destructive)
# ----------------------------------------

def enrich_metadata(input_yaml: dict | None, output_file: str | None = None):
    """
    New architecture:
    - Do NOT infer themes
    - Do NOT infer market_cap_style
    - Do NOT normalise sector/sub_sector (already normalised)
    - Do NOT generate theme_count
    - Do NOT generate inferred_themes
    - Only compute innovation_score if missing
    - Preserve all curated fields exactly
    - Return None if input is None
    - Only write output file if explicitly provided
    """

    if input_yaml is None:
        return None

    enriched = {}

    for symbol, data in sorted(input_yaml.items()):
        asset_type = data.get("asset_type")
        role = data.get("role")
        role_category = data.get("role_category", role)
        sector = data.get("sector")
        sub_sector = data.get("sub_sector")
        themes = data.get("themes", [])
        conviction = data.get("conviction")
        quality = data.get("quality")
        market_cap_style = data.get("market_cap_style")

        # Compute innovation_score ONLY if conviction & quality exist
        if conviction is None or quality is None:
            innovation_score = None
        else:
            innovation_score = round((conviction + quality) / 2, 3)

        enriched[symbol] = {
            "asset_type": asset_type,
            "role": role,
            "role_category": role_category,
            "sector": sector,
            "sub_sector": sub_sector,
            "themes": themes,
            "conviction": conviction,
            "quality": quality,
            "innovation_score": innovation_score,
            "market_cap_style": market_cap_style,
        }

    # ----------------------------------------
    # Only write output if explicitly requested
    # ----------------------------------------
    if output_file:
        with open(output_file, "w") as f:
            yaml.dump(enriched, f, sort_keys=True)

    return enriched

# # ----------------------------------------
# # 3. CLI Execution
# # ----------------------------------------

# if __name__ == "__main__":
#     input_path = BASE_DIR / "config" / "metadata" / "stock_metadata.yaml"
#     output_path = BASE_DIR / "config" / "metadata" / "metadata_enriched.yaml"

#     with open(input_path, "r") as f:
#         raw = yaml.safe_load(f)

#     # Only writes output because output_path is passed
#     enrich_metadata(raw, output_file=output_path)
