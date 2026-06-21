import yaml
from pathlib import Path
from collections import defaultdict
from app.config.environment import (
    BASE_DIR
)

def generate_sector_preferences(metadata_path):
    metadata = yaml.safe_load(Path(metadata_path).read_text())

    # Collect all unique sub_sectors
    sectors = {info.get("sub_sector") for info in metadata.values() if info}

    # Define classification rules
    growth = {
        "SEMICONDUCTORS", "AI_SOFTWARE", "AI_INFRASTRUCTURE",
        "OPTICAL_NETWORKING", "EV_AUTONOMY", "FINTECH",
        "CLOUD", "DATA_PLATFORMS", "OBSERVABILITY"
    }
    defensives = {
        "CYBERSECURITY", "POWER_INFRASTRUCTURE", "MEMORY",
        "CONSUMER", "STAPLES"
    }

    prefs = defaultdict(dict)

    for sector in sectors:
        if sector in growth:
            prefs["RISK_ON"][sector] = 0.9 if sector != "SEMICONDUCTORS" else 1.0
            prefs["NEUTRAL"][sector] = 0.7
            prefs["RISK_OFF"][sector] = 0.3 if sector != "SEMICONDUCTORS" else 0.4
        elif sector in defensives:
            prefs["RISK_ON"][sector] = 0.8
            prefs["NEUTRAL"][sector] = 0.7
            prefs["RISK_OFF"][sector] = 0.6 if sector != "POWER_INFRASTRUCTURE" else 0.7
        else:
            # Default for unclassified sectors
            prefs["RISK_ON"][sector] = 0.7
            prefs["NEUTRAL"][sector] = 0.7
            prefs["RISK_OFF"][sector] = 0.5

    return dict(prefs)

# Usage
MACRO_SECTOR_PREFERENCES = generate_sector_preferences(
    BASE_DIR / "config" / "metadata" / "ticker_metadata.yaml"
)
print(MACRO_SECTOR_PREFERENCES)
