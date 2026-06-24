from unittest.mock import patch
from pathlib import Path

from app.engine.scoring_engine import (
    sector_quality_score,
    moat_score,
    theme_strength_score,
    macro_fit_score,
    market_cap_style_score,
    base_strength,
    assign_role_from_strength,
    compute_conviction_and_quality,
    process_stock_metadata,
)

#----------------------------------------
# 1. Sector Quality Tests
# ----------------------------------------


def test_sector_quality_score():
    assert sector_quality_score("SEMICONDUCTORS") == 1.00
    assert sector_quality_score("OPTICAL_NETWORKING") == 0.75
    assert sector_quality_score("UNKNOWN") == 0.40
    assert sector_quality_score("NON_EXISTENT") == 0.40

# ----------------------------------------
# 2. Theme Strength Tests
# ----------------------------------------


def test_theme_strength_score():
    assert theme_strength_score(["AI"], 1) > 0
    assert theme_strength_score(["AI", "CLOUD", "CYBERSECURITY"], 3) <= 0.75
    assert theme_strength_score([], 0) == 0.0

# ----------------------------------------
# 3. Macro Fit Tests
# ----------------------------------------


def test_macro_fit_score():
    assert macro_fit_score(["AI"]) >= 0.3
    assert macro_fit_score(["AI", "CLOUD"]) <= 1.0
    assert macro_fit_score([]) == 0.3

# ----------------------------------------
# 4. Market Cap Style Tests
# ----------------------------------------

def test_market_cap_style_score():
    assert market_cap_style_score("LARGE_CAPS") == 1.00
    assert market_cap_style_score("MID_CAPS") == 0.85
    assert market_cap_style_score("SMALL_CAPS") == 0.70
    assert market_cap_style_score("UNKNOWN") == 0.75

# ----------------------------------------
# 5. Base Strength Tests
# ----------------------------------------

def test_base_strength():
    entry = {
        "sub_sector": "SEMICONDUCTORS",
        "themes": ["AI", "CLOUD"],
        "theme_count": 2,
        "innovation_score": 0.8,
        "market_cap_style": "LARGE_CAPS",
    }

    strength = base_strength(entry)
    assert 0.6 < strength < 1.0
# ----------------------------------------
# 6. Role Assignment Tests
# ----------------------------------------


def test_role_assignment():
    assert assign_role_from_strength(0.85) == "CORE"
    assert assign_role_from_strength(0.70) == "HIGH_CONVICTION"
    assert assign_role_from_strength(0.55) == "SATELLITE"
    assert assign_role_from_strength(0.30) == "SPECULATIVE"

# ----------------------------------------
# 7. Full Scoring Pipeline Test
# ----------------------------------------

@patch("app.engine.scoring_engine.fetch_market_cap")
def test_compute_conviction_and_quality(mock_mcap):
    mock_mcap.return_value = 2_500_000_000_000  # simulate AAPL

    entry = {
        "sub_sector": "CONSUMER_ELECTRONICS",
        "themes": ["CONSUMER"],
        "theme_count": 1,
        "innovation_score": 0.5,
        "market_cap_style": "LARGE_CAPS",
    }

    conviction, quality, role = compute_conviction_and_quality("AAPL", entry)

    assert 0.3 < quality < 0.8
    assert 0.3 < conviction < 0.9
    assert role in ["CORE", "HIGH_CONVICTION", "SATELLITE", "SPECULATIVE"]

def test_moat_score():
    # High‑moat sectors
    assert moat_score("SEMICONDUCTORS") == 1.00
    assert moat_score("CYBERSECURITY") == 0.95
    assert moat_score("CLOUD") == 0.90

    # Mid‑moat sectors
    assert moat_score("OPTICAL_NETWORKING") == 0.75
    assert moat_score("MEMORY") == 0.80
    assert moat_score("CONSUMER_ELECTRONICS") == 0.65

    # Low‑moat or unknown sectors
    assert moat_score("UNKNOWN") == 0.50
    assert moat_score("NON_EXISTENT") == 0.50  # fallback

    # Type and range checks
    score = moat_score("SEMICONDUCTORS")
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0

# def test_scoring_engine_output_file():
#     # Input metadata file
#     input_path = Path("config/metadata/stock_metadata.yaml")
#     assert input_path.exists()

#     # Temporary output file
#     output_path = Path("config/metadata/scored_metadata.yaml")

#     # Run scoring engine
#     result = process_stock_metadata(input_path, output_path)

#     # Validate output file exists
#     assert output_path.exists()
#     assert output_path.stat().st_size > 0

#     # Validate returned dict
#     assert isinstance(result, dict)
#     assert len(result) > 0

#     # Validate one ticker
#     ticker = next(iter(result))
#     entry = result[ticker]

#     assert "conviction" in entry
#     assert "quality" in entry
#     assert "role" in entry

