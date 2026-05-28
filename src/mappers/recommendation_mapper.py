from src.models.recommendation import (
    Recommendation
)


class RecommendationMapper:

    @staticmethod
    def from_dataframe_row(
        row
    ):

        return Recommendation(

            symbol=row["symbol"],

            price=row["price"],

            ai_score=row["ai_score"],

            rating=row["rating"],

            sector=row["sector"],

            rsi=row["rsi"],

            ma50=row["ma50"],

            ma200=row["ma200"],

            bullish_trend=row[
                "bullish_trend"
            ],

            portfolio_fit_score=row[
                "portfolio_fit_score"
            ]
        )