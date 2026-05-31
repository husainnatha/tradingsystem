import pandas as pd


# -----------------------------------
# BUILD DECISION ENGINE
# -----------------------------------

def build_decisions(

    action_df,

    risk_intelligence_df,

    tax_df
):

    rows = []

    for _, row in action_df.iterrows():

        rows.append({

            "symbol":
                row["symbol"],

            "decision":
                row["action"],

            "priority":
                row["priority"],

            "trade_value":
                row["trade_value"],

            "reason":
                row["reason"]
        })

    return pd.DataFrame(

        rows
    )