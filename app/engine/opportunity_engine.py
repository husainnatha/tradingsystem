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

        # --------------------
        # Explanation
        # --------------------

        explanation_parts = []

        if row["bullish_trend"]:

            explanation_parts.append(
                "Bullish trend"
            )
        if row["technical_score"] > 0.8:

            explanation_parts.append(
                f"Technical score {row['technical_score']:.2f}"
            )   
        
        if row["ai_score"] > 0.8:

            explanation_parts.append(
                f"AI score {row['ai_score']:.2f}"
            )

        if row["portfolio_fit_score"] > 0.8:

            explanation_parts.append(
                f"Portfolio fit {row['portfolio_fit_score']:.2f}"
            )

        if row["diversification_score"] > 0.4:

            explanation_parts.append(
                "Diversification benefit"
            )

        if row["macro_score"] > 0.8:

            explanation_parts.append(
                "Favourable macro environment"
            )
        
        if row["rsi"] < 40:

            explanation_parts.append(
                "Potentially oversold"
            )
        
        if row["momentum_score"] > 0.8:

            explanation_parts.append(
                "Strong momentum"
            )

        if row["rating"] == "STRONG":

            explanation_parts.append(
                "Strong rating"
            )

        if len(explanation_parts) == 0:

            explanation_parts.append(
                "No strong signals"
            )
            

        explanation = ", ".join(
            explanation_parts
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
                row["diversification_score"],

            "explanation":
                explanation
        })
    
    opportunity_df = pd.DataFrame(rows)

    opportunity_df = opportunity_df.sort_values(
        by="opportunity_score",
        ascending=False
    )

    return (opportunity_df)