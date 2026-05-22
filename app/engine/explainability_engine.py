# -----------------------------------
# GENERATE EXPLANATION
# -----------------------------------

def explain_position(row):

    explanations = []

    # -----------------------------------
    # TAX EFFICIENCY
    # -----------------------------------

    if row[
        "tax_efficiency_score"
    ] >= 0.7:

        explanations.append(

            "high tax efficiency"
        )

    elif row[
        "tax_efficiency_score"
    ] <= 0.3:

        explanations.append(

            "high potential tax impact"
        )

    # -----------------------------------
    # UNREALISED GAIN / LOSS
    # -----------------------------------

    if row[
        "unrealised_gain_gbp"
    ] < 0:

        explanations.append(

            "unrealised losses available"
        )

    elif row[
        "unrealised_gain_gbp"
    ] > 1000:

        explanations.append(

            "large unrealised gains"
        )

    # -----------------------------------
    # POSITION RISK
    # -----------------------------------

    if row[
        "position_risk_score"
    ] >= 0.7:

        explanations.append(

            "high concentration risk"
        )

    elif row[
        "position_risk_score"
    ] <= 0.3:

        explanations.append(

            "low concentration risk"
        )

    # -----------------------------------
    # HOLDING PERIOD
    # -----------------------------------

    if row[
        "holding_period_score"
    ] >= 0.7:

        explanations.append(

            "long holding period"
        )

    # -----------------------------------
    # FALLBACK
    # -----------------------------------

    if not explanations:

        explanations.append(

            "balanced portfolio profile"
        )

    # -----------------------------------
    # BUILD FINAL EXPLANATION
    # -----------------------------------

    return (

        "Recommended because of "

        +

        ", ".join(explanations)

        +

        "."
    )