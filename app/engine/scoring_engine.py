import yaml
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
    "OPTICAL_NETWORKING": 0.70,
    "CONSUMER ELECTRONICS": 0.60,
    "INDUSTRIALS": 0.55,
    "CONSUMER CYCLICAL": 0.45,
    "UNKNOWN": 0.30,
}

THEME_WEIGHTS = {
    "AI": 0.40,
    "CLOUD": 0.25,
    "CYBERSECURITY": 0.25,
    "DATA_CENTRES": 0.20,
    "PHOTONICS": 0.15,
    "NETWORKING": 0.15,
    "MEMORY": 0.15,
}

MOAT_SCORES = {
    "SEMICONDUCTORS": 1.00,
    "CYBERSECURITY": 0.95,
    "CLOUD": 0.90,
    "AI_INFRASTRUCTURE": 0.85,
    "OBSERVABILITY": 0.80,
    "OPTICAL_NETWORKING": 0.65,
    "CONSUMER ELECTRONICS": 0.55,
    "UNKNOWN": 0.40,
}

MACRO_FIT = {
    "SEMICONDUCTORS": 1.00,
    "CYBERSECURITY": 0.90,
    "CLOUD": 0.85,
    "AI_INFRASTRUCTURE": 0.85,
    "DATA_PLATFORMS": 0.80,
    "OPTICAL_NETWORKING": 0.60,
    "CONSUMER CYCLICAL": 0.40,
    "UNKNOWN": 0.30,
}

# -----------------------------
# 2. Market Cap Buckets
# -----------------------------

def market_cap_score(mcap):
    if mcap is None:
        return 0.40
    if mcap > 1_000_000_000_000:
        return 1.00
    if mcap > 200_000_000_000:
        return 0.90
    if mcap > 50_000_000_000:
        return 0.80
    if mcap > 10_000_000_000:
        return 0.65
    if mcap > 2_000_000_000:
        return 0.50
    return 0.35

# -----------------------------
# 3. Theme Score
# -----------------------------

def theme_score(themes):
    if not themes:
        return 0.0
    score = sum(THEME_WEIGHTS.get(t, 0.05) for t in themes)
    return min(score, 1.0)

# -----------------------------
# 4. Fetch Market Cap
# -----------------------------

def fetch_market_cap(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info.get("marketCap")
    except:
        return None

# -----------------------------
# 5. Role Assignment
# -----------------------------

def assign_role(base_strength):
    if base_strength >= 0.80:
        return "CORE"
    if base_strength >= 0.65:
        return "HIGH_CONVICTION"
    if base_strength >= 0.45:
        return "SATELLITE"
    return "SPECULATIVE"

# -----------------------------
# 6. Compute Scores
# -----------------------------

def compute_scores(ticker, entry):
    sector = entry.get("sub_sector", "UNKNOWN").upper()
    themes = entry.get("themes", [])

    S = SECTOR_QUALITY.get(sector, 0.30)
    T = theme_score(themes)
    O = MOAT_SCORES.get(sector, 0.40)

    mcap = fetch_market_cap(ticker)
    M = market_cap_score(mcap)

    base_strength = 0.40*M + 0.30*S + 0.30*T
    role = assign_role(base_strength)

    F = MACRO_FIT.get(sector, 0.30)

    quality = 0.35*S + 0.25*T + 0.25*M + 0.15*O
    conviction = 0.40*F + 0.30*(1 if role == "CORE" else 0.85 if role == "HIGH_CONVICTION" else 0.65 if role == "SATELLITE" else 0.45) + 0.20*T + 0.10*M

    return round(conviction, 3), round(quality, 3), role

# -----------------------------
# 7. Main Processing
# -----------------------------

def process_yaml(input_file, output_file):
    with open(input_file) as f:
        raw = yaml.safe_load(f)

    stocks = {}
    etfs = {}

    ETF_LIST = ["ARKK", "IWM", "QQQ", "SMH", "SOXX", "SPY"]

    for ticker, entry in raw.items():
        if ticker in ETF_LIST:
            entry["asset_type"] = "ETF"
            etfs[ticker] = entry
            continue

        entry["asset_type"] = "STOCK"

        conviction, quality, role = compute_scores(ticker, entry)
        entry["conviction"] = conviction
        entry["quality"] = quality
        entry["role"] = role

        stocks[ticker] = entry

    output = {"stocks": stocks, "etfs": etfs}

    with open(output_file, "w") as f:
        yaml.dump(output, f, sort_keys=True)

    print("Done.")

