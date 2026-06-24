import yaml
from pathlib import Path
import yfinance as yf

# -----------------------------
# 1. Scoring Tables
# -----------------------------

SECTOR_QUALITY = {
    "SEMICONDUCTORS": 1.00,
    "CYBERSECURITY": 0.95,
    "CLOUD": 0.90,
    "DATA_PLATFORMS": 0.90,
    "AI_INFRASTRUCTURE": 0.85,
    "OBSERVABILITY": 0.80,
    "OPTICAL_NETWORKING": 0.75,
    "MEMORY": 0.75,
    "POWER_INFRASTRUCTURE": 0.70,
    "DATA_PLATFORMS": 0.70,
    "CONSUMER_ELECTRONICS": 0.60,
    "INFORMATION_TECHNOLOGY_SERVICES": 0.60,
    "ADVERTISING_AGENCIES": 0.55,
    "INTERNET_CONTENT_&_INFORMATION": 0.65,
    "AUTO_MANUFACTURERS": 0.55,
    "RESTAURANTS": 0.50,
    "HOUSEHOLD_&_PERSONAL_PRODUCTS": 0.55,
    "CAPITAL_MARKETS": 0.55,
    "BIOTECHNOLOGY": 0.60,
    "HEALTH_INFORMATION_SERVICES": 0.60,
    "SPECIALTY_INDUSTRIAL_MACHINERY": 0.60,
    "UNKNOWN": 0.40,
}

MOAT_SCORES = {
    "SEMICONDUCTORS": 1.00,
    "CYBERSECURITY": 0.95,
    "CLOUD": 0.90,
    "AI_INFRASTRUCTURE": 0.90,
    "DATA_PLATFORMS": 0.85,
    "OBSERVABILITY": 0.80,
    "OPTICAL_NETWORKING": 0.75,
    "MEMORY": 0.80,
    "POWER_INFRASTRUCTURE": 0.75,
    "INTERNET_CONTENT_&_INFORMATION": 0.80,
    "CONSUMER_ELECTRONICS": 0.65,
    "CAPITAL_MARKETS": 0.65,
    "BIOTECHNOLOGY": 0.75,
    "SPECIALTY_INDUSTRIAL_MACHINERY": 0.70,
    "UNKNOWN": 0.50,
}

MACRO_THEME_WEIGHTS = {
    "AI": 0.25,
    "CLOUD": 0.20,
    "CYBERSECURITY": 0.20,
    "DATA_CENTRES": 0.15,
    "SEMICONDUCTORS": 0.20,
    "NETWORKING": 0.10,
    "PHOTONICS": 0.10,
    "ENERGY": 0.10,
    "FINTECH": 0.10,
}

MARKET_CAP_STYLE_SCORES = {
    "LARGE_CAPS": 1.00,
    "MID_CAPS": 0.85,
    "SMALL_CAPS": 0.70,
}

# -----------------------------
# 2. Market Cap (optional refinement)
# -----------------------------

def fetch_market_cap(ticker: str) -> float | None:
    try:
        info = yf.Ticker(ticker).fast_info
        return getattr(info, "market_cap", None)
    except Exception:
        return None

def market_cap_score_from_value(mcap: float | None) -> float:
    if mcap is None:
        return 0.60
    if mcap > 1_000_000_000_000:
        return 1.00
    if mcap > 200_000_000_000:
        return 0.90
    if mcap > 50_000_000_000:
        return 0.80
    if mcap > 10_000_000_000:
        return 0.70
    if mcap > 2_000_000_000:
        return 0.60
    return 0.50

# -----------------------------
# 3. Theme Scores
# -----------------------------

def theme_strength_score(themes: list[str], theme_count: int) -> float:
    if not themes:
        return 0.0
    base = min(theme_count, 5) * 0.12  # cap at 0.6
    return min(base, 0.75)

def macro_fit_score(themes: list[str]) -> float:
    if not themes:
        return 0.3
    score = sum(MACRO_THEME_WEIGHTS.get(t, 0.0) for t in themes)
    return min(max(score, 0.3), 1.0)

# -----------------------------
# 4. Core component scores
# -----------------------------

def sector_quality_score(sub_sector: str) -> float:
    return SECTOR_QUALITY.get(sub_sector, SECTOR_QUALITY["UNKNOWN"])

def moat_score(sub_sector: str) -> float:
    return MOAT_SCORES.get(sub_sector, MOAT_SCORES["UNKNOWN"])

def market_cap_style_score(style: str) -> float:
    return MARKET_CAP_STYLE_SCORES.get(style, 0.75)

# -----------------------------
# 5. Base strength & role
# -----------------------------

def base_strength(entry: dict) -> float:
    sub_sector = entry["sub_sector"]
    themes = entry.get("themes", [])
    theme_count = entry.get("theme_count", len(themes))
    innovation = entry.get("innovation_score", 0.5)
    market_cap_style = entry.get("market_cap_style", "MID_CAPS")

    SQS = sector_quality_score(sub_sector)
    TSS = theme_strength_score(themes, theme_count)
    INS = innovation
    MCS = market_cap_style_score(market_cap_style)
    MS = moat_score(sub_sector)

    return (
        0.30 * SQS +
        0.25 * TSS +
        0.20 * INS +
        0.15 * MCS +
        0.10 * MS
    )

def assign_role_from_strength(strength: float) -> str:
    if strength >= 0.80:
        return "CORE"
    if strength >= 0.65:
        return "HIGH_CONVICTION"
    if strength >= 0.50:
        return "SATELLITE"
    return "SPECULATIVE"

# -----------------------------
# 6. Conviction & Quality
# -----------------------------

def compute_conviction_and_quality(ticker: str, entry: dict) -> tuple[float, float, str]:
    sub_sector = entry["sub_sector"]
    themes = entry.get("themes", [])
    theme_count = entry.get("theme_count", len(themes))
    innovation = entry.get("innovation_score", 0.5)
    market_cap_style = entry.get("market_cap_style", "MID_CAPS")

    SQS = sector_quality_score(sub_sector)
    TSS = theme_strength_score(themes, theme_count)
    INS = innovation
    MCS = market_cap_style_score(market_cap_style)
    MS = moat_score(sub_sector)
    MFS = macro_fit_score(themes)

    strength = base_strength(entry)
    role = assign_role_from_strength(strength)

    role_factor = {
        "CORE": 1.00,
        "HIGH_CONVICTION": 0.90,
        "SATELLITE": 0.75,
        "SPECULATIVE": 0.60,
    }.get(role, 0.70)

    quality = (
        0.35 * SQS +
        0.25 * MS +
        0.20 * INS +
        0.20 * MCS
    )

    conviction = (
        0.35 * MFS +
        0.25 * role_factor +
        0.20 * INS +
        0.20 * TSS
    )

    return round(conviction, 3), round(quality, 3), role

# -----------------------------
# 7. Main processing
# -----------------------------

def process_stock_metadata(input_file: str | Path, output_file: str | Path | None = None):
    input_path = Path(input_file)
    with open(input_path, "r") as f:
        raw = yaml.safe_load(f)

    enriched = {}

    for ticker, entry in raw.items():
        conviction, quality, role = compute_conviction_and_quality(ticker, entry)
        entry["conviction"] = conviction
        entry["quality"] = quality
        entry["role"] = role
        entry["role_category"] = role  # keep aligned
        enriched[ticker] = entry

    if output_file is not None:
        out_path = Path(output_file)
        with open(out_path, "w") as f:
            yaml.dump(enriched, f, sort_keys=False)

    return enriched

# if __name__ == "__main__":
#     # Example usage:
#     #input_file = "config/metadata/stock_metadata.yaml"
#     #output_file = "config/metadata/stock_metadata_scored.yaml"
#     process_stock_metadata(input_file)#, output_file)
#     print("Scoring complete.")
