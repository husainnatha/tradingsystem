"""
Tests for market_intelligence.py

Run with:
    pytest tests/test_market_intelligence.py -v

No live data, no network calls, no app dependencies — every external
service is replaced by a tiny fake or a simple stub.
"""

import pandas as pd
import pytest

from app.engine.market_intelligence_engine import (
    build_market_intelligence
)


# ===========================================================================
# FIXTURES — shared test data
# ===========================================================================

@pytest.fixture
def bullish_symbol_df():
    """A minimal DataFrame where MA50 > MA200 (bullish trend)."""
    return pd.DataFrame([{
        "Close": 150.0,
        "MA50":  160.0,
        "MA200": 140.0,
        "RSI":    55.0,
    }])


@pytest.fixture
def bearish_symbol_df():
    """A minimal DataFrame where MA50 < MA200 (bearish trend)."""
    return pd.DataFrame([{
        "Close": 90.0,
        "MA50":  85.0,
        "MA200": 100.0,
        "RSI":   70.0,
    }])


@pytest.fixture
def market_context_stub(bullish_symbol_df, bearish_symbol_df):
    """
    A lightweight stand-in for the real MarketContext object.
    Exposes two symbols — one bullish, one bearish.
    """
    class _MarketContext:
        def get_all(self):
            return {
                "AAPL": bullish_symbol_df,
                "XYZ":  bearish_symbol_df,
            }
    return _MarketContext()


# ---------------------------------------------------------------------------
# Helpers that replace the real infrastructure callables
# ---------------------------------------------------------------------------

def _macro_risk_on():
    return {"regime": "RISK_ON"}

def _macro_risk_off():
    return {"regime": "RISK_OFF"}

def _macro_neutral():
    return {"regime": "NEUTRAL"}

def _sector_exposure():
    return pd.DataFrame([
        {"sector": "Technology", "exposure_pct": 30},
        {"sector": "Energy",     "exposure_pct": 10},
    ])

def _correlation_engine(market_context):
    return pd.DataFrame([
        {"symbol": "AAPL", "diversification_score": 0.7},
        {"symbol": "XYZ",  "diversification_score": 0.4},
    ])

def _get_sector(symbol):
    return {"AAPL": "Technology", "XYZ": "Energy"}.get(symbol, "Unknown")

def _get_sector_bias(regime, sector):
    return 0.6 if sector == "Technology" else 0.3


# ===========================================================================
# UNIT TESTS — pure scoring functions
# ===========================================================================

class TestComputeMomentumScore:
    def test_bullish_returns_one(self):
        assert momentum_score(True) == 1

    def test_bearish_returns_zero(self):
        assert momentum_score(False) == 0


class TestComputeRsiScore:
    def test_rsi_50_gives_half(self):
        assert rsi_score(50) == pytest.approx(0.5)

    def test_rsi_0_gives_one(self):
        assert rsi_score(0) == pytest.approx(1.0)

    def test_rsi_100_gives_zero(self):
        assert rsi_score(100) == pytest.approx(0.0)

    def test_lower_rsi_scores_higher(self):
        assert rsi_score(30) > rsi_score(70)


class TestComputePortfolioFitScore:
    def test_zero_exposure_is_perfect_fit(self):
        assert portfolio_fit_score(0) == pytest.approx(1.0)

    def test_full_exposure_is_zero_fit(self):
        assert portfolio_fit_score(100) == pytest.approx(0.0)

    def test_over_100_is_clamped_to_zero(self):
        assert portfolio_fit_score(150) == pytest.approx(0.0)

    def test_partial_exposure_is_proportional(self):
        assert portfolio_fit_score(40) == pytest.approx(0.6)


class TestComputeMacroScore:
    @pytest.mark.parametrize("momentum,expected", [(1, 1.0), (0, 0.25)])
    def test_risk_on(self, momentum, expected):
        assert macro_score("RISK_ON", momentum) == pytest.approx(expected)

    @pytest.mark.parametrize("momentum,expected", [(1, 0.2), (0, 0.8)])
    def test_risk_off(self, momentum, expected):
        assert macro_score("RISK_OFF", momentum) == pytest.approx(expected)

    def test_neutral_regime(self):
        assert macro_score("NEUTRAL", 1) == pytest.approx(0.5)
        assert macro_score("NEUTRAL", 0) == pytest.approx(0.5)

    def test_unknown_regime_defaults_to_neutral(self):
        assert macro_score("SIDEWAYS", 1) == pytest.approx(0.5)


class TestComputeTechnicalScore:
    def test_both_max(self):
        assert technical_score(1, 1.0) == pytest.approx(1.0)

    def test_both_zero(self):
        assert technical_score(0, 0.0) == pytest.approx(0.0)

    def test_average(self):
        assert technical_score(1, 0.5) == pytest.approx(0.75)

    def test_rounding_to_4dp(self):
        # 1 + 0.333... / 2 = 0.6667 rounded to 4 dp
        score = technical_score(1, 1/3)
        assert score == round((1 + 1/3) / 2, 4)


class TestComputeAiScore:
    def test_all_ones_returns_one(self):
        assert ai_score(1.0, 1.0, 1.0, 1.0, 1.0) == pytest.approx(1.0)

    def test_all_zeros_returns_zero(self):
        assert ai_score(0.0, 0.0, 0.0, 0.0, 0.0) == pytest.approx(0.0)

    def test_weights_sum_to_one(self):
        # Weights: 0.30 + 0.20 + 0.15 + 0.15 + 0.20 = 1.0
        # Score with inputs equal to their weight value should equal
        # sum of weight² — just check the known weights add to 1 via max score.
        assert ai_score(1, 1, 1, 1, 1) == pytest.approx(1.0)

    def test_known_values(self):
        result = ai_score(
            technical_score=0.8,
            macro_score=0.6,
            portfolio_fit_score=0.5,
            diversification_score=0.7,
            sector_bias=0.4,
        )
        expected = round(0.8*0.30 + 0.6*0.20 + 0.5*0.15 + 0.7*0.15 + 0.4*0.20, 4)
        assert result == pytest.approx(expected)


class TestComputeRating:
    def test_strong_rating(self):
        assert rating(ai_score=0.85, portfolio_fit_score=0.7) == "STRONG"

    def test_strong_requires_both_conditions(self):
        # High ai_score but low portfolio fit → BUY, not STRONG
        assert rating(ai_score=0.85, portfolio_fit_score=0.5) == "BUY"

    def test_buy_rating(self):
        assert rating(ai_score=0.65, portfolio_fit_score=0.3) == "BUY"

    def test_watch_rating(self):
        assert rating(ai_score=0.45, portfolio_fit_score=0.3) == "WATCH"

    def test_avoid_rating(self):
        assert rating(ai_score=0.2, portfolio_fit_score=0.1) == "AVOID"

    @pytest.mark.parametrize("ai_score,fit,expected", [
        (0.80, 0.60, "STRONG"),
        (0.79, 0.60, "BUY"),
        (0.80, 0.59, "BUY"),
        (0.60, 0.00, "BUY"),
        (0.59, 0.99, "WATCH"),
        (0.40, 0.00, "WATCH"),
        (0.39, 0.99, "AVOID"),
    ])
    def test_boundary_conditions(self, ai_score, fit, expected):
        assert rating(ai_score, fit) == expected


# ===========================================================================
# UNIT TESTS — extract_symbol_data
# ===========================================================================

class TestExtractSymbolData:
    def test_bullish_trend_detected(self, bullish_symbol_df):
        data = extract_symbol_data(bullish_symbol_df)
        assert data["bullish_trend"] is True

    def test_bearish_trend_detected(self, bearish_symbol_df):
        data = extract_symbol_data(bearish_symbol_df)
        assert data["bearish_trend"] if "bearish_trend" in data else not data["bullish_trend"]

    def test_price_extracted(self, bullish_symbol_df):
        data = extract_symbol_data(bullish_symbol_df)
        assert data["price"] == pytest.approx(150.0)

    def test_ma_values_extracted(self, bullish_symbol_df):
        data = extract_symbol_data(bullish_symbol_df)
        assert data["ma50"]  == pytest.approx(160.0)
        assert data["ma200"] == pytest.approx(140.0)

    def test_rsi_extracted(self, bullish_symbol_df):
        data = extract_symbol_data(bullish_symbol_df)
        assert data["rsi"] == pytest.approx(55.0)

    def test_equal_mas_not_bullish(self):
        df = pd.DataFrame([{"Close": 100.0, "MA50": 100.0, "MA200": 100.0, "RSI": 50.0}])
        data = extract_symbol_data(df)
        assert data["bullish_trend"] is False


# ===========================================================================
# UNIT TESTS — score_symbol (integration of all pure functions)
# ===========================================================================

class TestScoreSymbol:
    def _bullish_data(self):
        return {"price": 150.0, "ma50": 160.0, "ma200": 140.0,
                "rsi": 55.0, "bullish_trend": True}

    def test_output_keys_present(self):
        result = score_symbol("AAPL", self._bullish_data(), "RISK_ON", 30, 0.7, 0.6)
        expected_keys = {
            "symbol", "price", "ma50", "ma200", "rsi", "bullish_trend",
            "momentum_score", "rsi_score", "technical_score",
            "macro_regime", "macro_score",
            "portfolio_exposure", "portfolio_fit_score",
            "diversification_score", "sector_bias",
            "ai_score", "rating",
        }
        assert expected_keys.issubset(result.keys())

    def test_symbol_preserved(self):
        result = score_symbol("AAPL", self._bullish_data(), "RISK_ON", 30, 0.7, 0.6)
        assert result["symbol"] == "AAPL"

    def test_regime_preserved(self):
        result = score_symbol("AAPL", self._bullish_data(), "RISK_OFF", 10, 0.5, 0.4)
        assert result["macro_regime"] == "RISK_OFF"

    def test_scores_are_floats(self):
        result = score_symbol("AAPL", self._bullish_data(), "RISK_ON", 30, 0.7, 0.6)
        for key in ("ai_score", "technical_score", "macro_score", "rsi_score"):
            assert isinstance(result[key], float), f"{key} should be float"

    def test_ai_score_bounded(self):
        result = score_symbol("AAPL", self._bullish_data(), "RISK_ON", 0, 1.0, 1.0)
        assert 0.0 <= result["ai_score"] <= 1.0


# ===========================================================================
# INTEGRATION TESTS — build_market_intelligence
# ===========================================================================

class TestBuildMarketIntelligence:
    def test_returns_dataframe(self, market_context_stub):
        df = build_market_intelligence(
            market_context_stub,
            build_macro_regime_fn=_macro_risk_on,
            build_sector_exposure_fn=_sector_exposure,
            build_correlation_engine_fn=_correlation_engine,
            get_sector_fn=_get_sector,
            get_sector_bias_fn=_get_sector_bias,
        )
        assert isinstance(df, pd.DataFrame)

    def test_one_row_per_symbol(self, market_context_stub):
        df = build_market_intelligence(
            market_context_stub,
            build_macro_regime_fn=_macro_risk_on,
            build_sector_exposure_fn=_sector_exposure,
            build_correlation_engine_fn=_correlation_engine,
            get_sector_fn=_get_sector,
            get_sector_bias_fn=_get_sector_bias,
        )
        assert len(df) == 2
        assert set(df["symbol"]) == {"AAPL", "XYZ"}

    def test_sorted_by_ai_score_descending(self, market_context_stub):
        df = build_market_intelligence(
            market_context_stub,
            build_macro_regime_fn=_macro_risk_on,
            build_sector_exposure_fn=_sector_exposure,
            build_correlation_engine_fn=_correlation_engine,
            get_sector_fn=_get_sector,
            get_sector_bias_fn=_get_sector_bias,
        )
        scores = df["ai_score"].tolist()
        assert scores == sorted(scores, reverse=True)

    def test_sector_attached_to_rows(self, market_context_stub):
        df = build_market_intelligence(
            market_context_stub,
            build_macro_regime_fn=_macro_risk_on,
            build_sector_exposure_fn=_sector_exposure,
            build_correlation_engine_fn=_correlation_engine,
            get_sector_fn=_get_sector,
            get_sector_bias_fn=_get_sector_bias,
        )
        assert "sector" in df.columns
        assert df.loc[df["symbol"] == "AAPL", "sector"].iloc[0] == "Technology"
        assert df.loc[df["symbol"] == "XYZ",  "sector"].iloc[0] == "Energy"

    def test_unknown_symbol_uses_default_exposure(self, market_context_stub):
        """Symbols missing from sector_lookup default to 0 % exposure."""
        def _no_exposure():
            return pd.DataFrame(columns=["sector", "exposure_pct"])

        df = build_market_intelligence(
            market_context_stub,
            build_macro_regime_fn=_macro_risk_on,
            build_sector_exposure_fn=_no_exposure,
            build_correlation_engine_fn=_correlation_engine,
            get_sector_fn=_get_sector,
            get_sector_bias_fn=_get_sector_bias,
        )
        # With 0 % exposure, portfolio_fit_score should be 1.0 for all rows.
        assert (df["portfolio_fit_score"] == 1.0).all()

    def test_unknown_symbol_uses_default_diversification(self, market_context_stub):
        """Symbols missing from correlation data default to 0.5."""
        def _empty_correlation(mc):
            return pd.DataFrame(columns=["symbol", "diversification_score"])

        df = build_market_intelligence(
            market_context_stub,
            build_macro_regime_fn=_macro_risk_on,
            build_sector_exposure_fn=_sector_exposure,
            build_correlation_engine_fn=_empty_correlation,
            get_sector_fn=_get_sector,
            get_sector_bias_fn=_get_sector_bias,
        )
        assert (df["diversification_score"] == 0.5).all()

    @pytest.mark.parametrize("regime_fn,expected_regime", [
        (_macro_risk_on,  "RISK_ON"),
        (_macro_risk_off, "RISK_OFF"),
        (_macro_neutral,  "NEUTRAL"),
    ])
    def test_regime_propagated_to_rows(self, market_context_stub, regime_fn, expected_regime):
        df = build_market_intelligence(
            market_context_stub,
            build_macro_regime_fn=regime_fn,
            build_sector_exposure_fn=_sector_exposure,
            build_correlation_engine_fn=_correlation_engine,
            get_sector_fn=_get_sector,
            get_sector_bias_fn=_get_sector_bias,
        )
        assert (df["macro_regime"] == expected_regime).all()

    def test_all_ratings_are_valid(self, market_context_stub):
        df = build_market_intelligence(
            market_context_stub,
            build_macro_regime_fn=_macro_risk_on,
            build_sector_exposure_fn=_sector_exposure,
            build_correlation_engine_fn=_correlation_engine,
            get_sector_fn=_get_sector,
            get_sector_bias_fn=_get_sector_bias,
        )
        assert set(df["rating"]).issubset({"STRONG", "BUY", "WATCH", "AVOID"})