import pandas as pd


def build_opportunities(

    market_intelligence_df
):

    rows = []

    for _, row in (

        market_intelligence_df
        .iterrows()
    ):

        score = 0

        # --------------------
        # AI SCORE
        # --------------------

        score += (

            row["ai_score"]

            * 40
        )

        # --------------------
        # TECHNICALS
        # --------------------

        if (

            row[
                "technical_score"
            ] > 0.7
        ):

            score += 20

        # --------------------
        # PORTFOLIO FIT
        # --------------------

        score += (

            row[
                "portfolio_fit_score"
            ]

            * 20
        )

        # --------------------
        # MACRO
        # --------------------

        score += (

            row[
                "macro_score"
            ]

            * 20
        )

        rows.append({

            "symbol":

                row[
                    "symbol"
                ],

            "rating":

                row[
                    "rating"
                ],

            "opportunity_score":

                round(
                    score,
                    2
                ),
                
            "ai_score":
                row["ai_score"],

            "technical_score":
                row["technical_score"],

            "portfolio_fit_score":
                row["portfolio_fit_score"],

            "macro_score":
                row["macro_score"],

            "diversification_score":
                row["diversification_score"]
        })

    return (

        pd.DataFrame(rows)

        .sort_values(

            by=
                "opportunity_score",

            ascending=False
        )

        .head(30)
    )

