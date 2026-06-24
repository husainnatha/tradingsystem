import yaml

from app.config.environment import (
    BASE_DIR
)

THEMES = [
    "AI", "PHOTONICS", "SEMICONDUCTORS", "NETWORKING", "DATA_CENTRES",
    "CYBERSECURITY", "QUANTUM", "AUTONOMY", "ROBOTICS", "HEALTHCARE",
    "ENERGY", "FINTECH", "CLOUD", "AUTOMATION", "CONSUMER", "DEFENSIVE",
    "STREAMING", "ENTERTAINMENT", "SMALL_CAPS", "INNOVATION", "MARKET"
]

def normalize_sector(value: str) -> str:
    return value.upper().replace(" ", "_")

def normalize_subsector(value: str) -> str:
    return value.upper().replace(" ", "_").replace("-", "_")

def infer_market_cap_style(symbol: str) -> str:
    # Placeholder heuristic — replace with real market cap logic later
    if symbol.isupper() and len(symbol) <= 4:
        return "LARGE_CAPS"
    return "SMALL_CAPS"

def option_b_themes(sector, sub_sector, existing):
    themes = set(existing)

    if "SEMICONDUCTOR" in sub_sector:
        themes.update(["SEMICONDUCTORS", "INNOVATION"])

    if "CLOUD" in sub_sector or sector == "TECHNOLOGY":
        themes.add("CLOUD")

    if "AI" in sub_sector:
        themes.add("AI")

    if "NETWORK" in sub_sector:
        themes.add("NETWORKING")

    if "OPTICAL" in sub_sector:
        themes.add("PHOTONICS")

    if "CYBER" in sub_sector:
        themes.add("CYBERSECURITY")

    if "DATA" in sub_sector:
        themes.add("DATA_CENTRES")

    if "CONSUMER" in sub_sector:
        themes.add("CONSUMER")

    return sorted(t for t in themes if t in THEMES)

def option_c_inferred_themes(sector, sub_sector, themes, market_cap_style):
    inferred = set()

    # Broad inference rules
    if sector == "TECHNOLOGY":
        inferred.update(["AI", "AUTOMATION", "INNOVATION", "MARKET"])

    if "SEMICONDUCTOR" in sub_sector:
        inferred.update(["AI", "AUTOMATION", "INNOVATION"])

    if "CLOUD" in sub_sector:
        inferred.update(["AI", "AUTOMATION", "MARKET"])

    if "CYBER" in sub_sector:
        inferred.update(["DEFENSIVE", "CLOUD"])

    if "OPTICAL" in sub_sector:
        inferred.update(["PHOTONICS", "NETWORKING", "DATA_CENTRES"])

    if "ENTERTAINMENT" in sub_sector:
        inferred.update(["ENTERTAINMENT", "STREAMING"])

    if "AUTO" in sub_sector:
        inferred.update(["AUTONOMY", "ROBOTICS"])

    if market_cap_style == "SMALL_CAPS":
        inferred.add("SMALL_CAPS")

    # Remove curated themes
    inferred = inferred - set(themes)

    return sorted(t for t in inferred if t in THEMES)

def enrich_metadata(input_yaml: dict):
    output = {}

    for symbol, data in sorted(input_yaml.items()):
        sector = normalize_sector(data["sector"])
        sub_sector = normalize_subsector(data["sub_sector"])

        themes = option_b_themes(sector, sub_sector, data.get("themes", []))
        market_cap_style = infer_market_cap_style(symbol)
        inferred = option_c_inferred_themes(sector, sub_sector, themes, market_cap_style)

        innovation_score = round((data["conviction"] + data["quality"]) / 2, 3)

        output[symbol] = {
            "asset_type": data["asset_type"],
            "role": data["role"],
            "role_category": data["role"],
            "sector": sector,
            "sub_sector": sub_sector,
            "conviction": data["conviction"],
            "quality": data["quality"],
            "innovation_score": innovation_score,
            "market_cap_style": market_cap_style,
            "theme_count": len(themes),
            "themes": themes,
            "inferred_themes": inferred,
        }

    return output

if __name__ == "__main__":

    input_path = BASE_DIR / "config" / "metadata" / "stock_metadata.yaml"
    output_path = BASE_DIR / "config" / "metadata" / "metadata_enriched.yaml"

    with open(input_path, "r") as f:
        raw = yaml.safe_load(f)

    enriched = enrich_metadata(raw)

    with open(output_path, "w") as f:
        yaml.dump(enriched, f, sort_keys=True)
