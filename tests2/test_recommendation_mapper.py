import pandas as pd

from src.mappers.recommendation_mapper import (
    RecommendationMapper
)


def test_recommendation_mapper():

    row = pd.Series({

        "symbol": "GC=F",

        "price": 4500.0,

        "ai_score": 0.82,

        "rating": "BUY",

        "sector": "Metals",

        "rsi": 44.2,

        "ma50": 4600.0,

        "ma200": 4300.0,

        "bullish_trend": True,

        "portfolio_fit_score": 0.75,

        "diversification_score": 0.62,

        "macro_score": 0.80
    })

    recommendation = (
        RecommendationMapper
        .from_dataframe_row(row)
    )

    assert recommendation.symbol == "GC=F"

    assert recommendation.ai_score == 0.82

    assert recommendation.rating == "BUY"

    assert recommendation.bullish_trend is True