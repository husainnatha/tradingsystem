from unittest.mock import patch
from app.engine.scoring_engine import compute_conviction_and_quality

def test_full_scoring_pipeline_with_fixtures(
    sample_stock_entry_semiconductors,
    sample_stock_entry_photonics,
    sample_stock_entry_consumer,
):
    """
    Full integration test for the scoring engine using fixtures and mocks.
    Ensures:
      - conviction and quality are computed
      - role assignment is correct
      - scores fall within expected ranges
      - structure is correct
    """

    with patch("app.engine.scoring_engine.fetch_market_cap") as mock_mcap:
        mock_mcap.return_value = 1_500_000_000_000  # simulate large-cap

        # --- SEMICONDUCTORS (high moat, high quality) ---
        conviction, quality, role = compute_conviction_and_quality(
            "AMD", sample_stock_entry_semiconductors
        )

        assert 0.4 < conviction <= 1.0
        assert 0.5 < quality <= 1.0
        assert role in ["CORE", "HIGH_CONVICTION"]

        # --- PHOTONICS (lower moat, small cap) ---
        conviction2, quality2, role2 = compute_conviction_and_quality(
            "LPTH", sample_stock_entry_photonics
        )

        assert 0.1 < conviction2 < conviction
        assert 0.1 < quality2 < quality
        assert role2 in ["SPECULATIVE", "SATELLITE"]

        # --- CONSUMER CYCLICAL (mid moat, mid cap) ---
        conviction3, quality3, role3 = compute_conviction_and_quality(
            "NKE", sample_stock_entry_consumer
        )

        assert 0.2 < conviction3 < 0.8
        assert 0.2 < quality3 < 0.8
        assert role3 in ["SATELLITE", "HIGH_CONVICTION", "SPECULATIVE"]

        # --- Structural checks ---
        for c, q, r in [
            (conviction, quality, role),
            (conviction2, quality2, role2),
            (conviction3, quality3, role3),
        ]:
            assert isinstance(c, float)
            assert isinstance(q, float)
            assert isinstance(r, str)
            assert 0.0 <= c <= 1.0
            assert 0.0 <= q <= 1.0
