from unittest.mock import patch
from app.engine.scoring_engine import (
    market_cap_score,
    theme_score,
    assign_role,
    compute_scores
)

# ----------------------------------------
# 1. Market Cap Score Tests
# ----------------------------------------

def test_market_cap_score_buckets():
    assert market_cap_score(2_000_000_000_000) == 1.00     # > 1T
    assert market_cap_score(300_000_000_000) == 0.90       # > 200B
    assert market_cap_score(80_000_000_000) == 0.80        # > 50B
    assert market_cap_score(20_000_000_000) == 0.65        # > 10B
    assert market_cap_score(5_000_000_000) == 0.50         # > 2B
    assert market_cap_score(500_000_000) == 0.35           # < 2B

# ----------------------------------------
# 2. Theme Score Tests
# ----------------------------------------

def test_theme_score_basic():
    assert theme_score(["AI"]) == 0.40
    assert theme_score(["AI", "CLOUD"]) == 0.65
    assert theme_score([]) == 0.0

def test_theme_score_cap_at_one():
    assert theme_score(["AI", "CLOUD", "CYBERSECURITY", "DATA_CENTRES"]) == 1.0

# ----------------------------------------
# 3. Role Assignment Tests
# ----------------------------------------

def test_role_assignment():
    assert assign_role(0.85) == "CORE"
    assert assign_role(0.70) == "HIGH_CONVICTION"
    assert assign_role(0.50) == "SATELLITE"
    assert assign_role(0.30) == "SPECULATIVE"

# ----------------------------------------
# 4. Full Scoring Pipeline Test
# ----------------------------------------

from unittest.mock import patch

@patch("app.engine.scoring_engine.fetch_market_cap")
def test_compute_scores(mock_mcap):
    mock_mcap.return_value = 2_500_000_000_000  # simulate AAPL

    entry = {
        "sub_sector": "Consumer Electronics",
        "themes": []
    }

    conviction, quality, role = compute_scores("AAPL", entry)

    assert 0.4 < quality < 0.7
    assert 0.4 < conviction < 0.75
    assert role == "SATELLITE"


