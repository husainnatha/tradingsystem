import yaml
from pathlib import Path
import yfinance as yf

# ============================================================
#  CANONICAL TAXONOMY — SECTOR / SUB_SECTOR / THEMES
# ============================================================

# -------------------------
# SECTORS
# -------------------------
# TECHNOLOGY
# COMMUNICATION_SERVICES
# CONSUMER_CYCLICAL
# CONSUMER_DEFENSIVE
# FINANCIAL_SERVICES
# INDUSTRIALS
# HEALTHCARE
# UTILITIES

# -------------------------
# SUB-SECTORS (TECHNOLOGY)
# -------------------------
# SEMICONDUCTORS
# MEMORY_CHIPS
# SEMICONDUCTOR_EQUIPMENT_AND_MATERIALS
# AI_INFRASTRUCTURE
# SOFTWARE_INFRASTRUCTURE
# SOFTWARE_APPLICATION
# CLOUD
# CYBERSECURITY
# COMPUTER_HARDWARE
# DATA_PLATFORMS
# COMMUNICATION_EQUIPMENT
# OPTICAL_NETWORKING
# PHOTONICS
# INFORMATION_TECHNOLOGY_SERVICES
# IT_SERVICES

# -------------------------
# SUB-SECTORS (OTHER SECTORS)
# -------------------------
# INTERNET_CONTENT_AND_INFORMATION
# ADVERTISING_AGENCIES
# INTERNET_RETAIL
# AUTO_MANUFACTURERS
# FOOTWEAR_AND_ACCESSORIES
# RESTAURANTS
# HOUSEHOLD_PRODUCTS
# CAPITAL_MARKETS
# BIOTECHNOLOGY
# SPECIALTY_INDUSTRIAL_MACHINERY
# ELECTRICAL_EQUIPMENT_AND_PARTS
# ROBOTICS
# UTILITIES_INDEPENDENT_POWER_PRODUCERS

# -------------------------
# THEMES
# -------------------------
# AI
# CLOUD
# DATA_CENTRES
# SEMICONDUCTORS
# MEMORY
# NETWORKING
# INNOVATION
# CYBERSECURITY
# PHOTONICS
# AUTOMATION
# ROBOTICS
# CONSUMER
# MARKET
# ENERGY
# DEFENSIVE
# ENTERTAINMENT
# STREAMING
# POWER_INFRASTRUCTURE
# INDUSTRIALS
# HEALTHCARE

# (Included here for reference — not used directly in code)
# See your YAML header for the full commented taxonomy.


# ============================================================
# 1. SCORING TABLES — ALIGNED WITH OPTION A
# ============================================================

SECTOR_QUALITY = {
    "SEMICONDUCTORS": 1.00,
    "MEMORY_CHIPS": 0.90,
    "SEMICONDUCTOR_EQUIPMENT_AND_MATERIALS": 0.90,
    "AI_INFRASTRUCTURE": 0.90,
    "SOFTWARE_INFRASTRUCTURE": 0.85,
    "SOFTWARE_APPLICATION": 0.80,
    "CLOUD": 0.85,
    "CYBERSECURITY": 0.95,
    "COMPUTER_HARDWARE": 0.80,
    "DATA_PLATFORMS": 0.85,
    "COMMUNICATION_EQUIPMENT": 0.75,
    "OPTICAL_NETWORKING": 0.75,
    "PHOTONICS": 0.70,
    "INFORMATION_TECHNOLOGY_SERVICES": 0.70,
    "IT_SERVICES": 0.70,

    "INTERNET_CONTENT_AND_INFORMATION": 0.75,
    "ADVERTISING_AGENCIES": 0.55,
    "INTERNET_RETAIL": 0.65,

    "AUTO_MANUFACTURERS": 0.60,
    "FOOTWEAR_AND_ACCESSORIES": 0.55,
    "RESTAURANTS": 0.50,

    "HOUSEHOLD_PRODUCTS": 0.55,
    "CAPITAL_MARKETS": 0.60,

    "BIOTECHNOLOGY": 0.65,

    "SPECIALTY_INDUSTRIAL_MACHINERY": 0.70,
    "ELECTRICAL_EQUIPMENT_AND_PARTS": 0.70,
    "ROBOTICS": 0.75,

    "UTILITIES_INDEPENDENT_POWER_PRODUCERS": 0.55,

    "UNKNOWN": 0.40,
}

MOAT_SCORES = {
    k: v for k, v in SECTOR_QUALITY.items()
}
MOAT_SCORES["SEMICONDUCTOR_EQUIPMENT_AND_MATERIALS"] = 0.95
MOAT_SCORES["CYBERSECURITY"] = 0.95
MOAT_SCORES["SEMICONDUCTORS"] = 1.00

MACRO_THEME_WEIGHTS = {
    "AI": 0.25,
    "CLOUD": 0.20,
    "CYBERSECURITY": 0.20,
    "DATA_CENTRES": 0.15,
    "SEMICONDUCTORS": 0.20,
    "MEMORY": 0.15,
    "NETWORKING": 0.10,
    "PHOTONICS": 0.10,
    "AUTOMATION": 0.10,
    "ROBOTICS": 0.10,
    "ENERGY": 0.10,
    "CONSUMER": 0.05,
    "MARKET": 0.05,
    "DEFENSIVE": 0.05,
    "ENTERTAINMENT": 0.05,
    "STREAMING": 0.05,
    "POWER_INFRASTRUCTURE": 0.10,
    "HEALTHCARE": 0.10,
}

MARKET_CAP_STYLE_SCORES = {
    "LARGE_CAPS": 1.00,
    "MID_CAPS": 0.85,
    "SMALL_CAPS": 0.70,
}


# ============================================================
# 2. MARKET CAP HELPERS
# ============================================================

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


# ============================================================
# 3. THEME SCORING
# ============================================================

def theme_strength_score(themes: list[str]) -> float:
    if not themes:
        return 0.0
    base = min(len(themes), 5) * 0.12
    return min(base, 0.75)

def macro_fit_score(themes: list[str]) -> float:
    if not themes:
        return 0.3
    score = sum(MACRO_THEME_WEIGHTS.get(t, 0.0) for t in themes)
    return min(max(score, 0.3), 1.0)


# ============================================================
# 4. CORE COMPONENT SCORES
# ============================================================

def sector_quality_score(sub_sector: str) -> float:
    return SECTOR_QUALITY.get(sub_sector, SECTOR_QUALITY["UNKNOWN"])

def moat_score(sub_sector: str) -> float:
    return MOAT_SCORES.get(sub_sector, MOAT_SCORES["UNKNOWN"])

def market_cap_style_score(style: str) -> float:
    return MARKET_CAP_STYLE_SCORES.get(style, 0.75)


# ============================================================
# 5. BASE STRENGTH + ROLE ASSIGNMENT
# ============================================================

def base_strength(entry: dict) -> float:
    sub_sector = entry["sub_sector"]
    themes = entry.get("themes", [])
    innovation = entry.get("innovation_score", 0.5)
    market_cap_style = entry.get("market_cap_style", "MID_CAPS")

    SQS = sector_quality_score(sub_sector)
    TSS = theme_strength_score(themes)
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


# ============================================================
# 6. CONVICTION + QUALITY
# ============================================================

def compute_conviction_and_quality(ticker: str, entry: dict) -> tuple[float, float, str]:
    sub_sector = entry["sub_sector"]
    themes = entry.get("themes", [])
    innovation = entry.get("innovation_score", 0.5)
    market_cap_style = entry.get("market_cap_style", "MID_CAPS")

    SQS = sector_quality_score(sub_sector)
    TSS = theme_strength_score(themes)
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


# ============================================================
# 7. MAIN PROCESSOR
# ============================================================

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
        entry["role_category"] = role
        enriched[ticker] = entry

    if output_file is not None:
        out_path = Path(output_file)
        with open(out_path, "w") as f:
            yaml.dump(enriched, f, sort_keys=False)

    return enriched
