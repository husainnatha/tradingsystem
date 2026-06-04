import pandas as pd

# -----------------------------------

# BUILD ACTION ENGINE

# -----------------------------------

def build_actions(

    rebalance_df,

    position_df,

    portfolio_risk_df,

    portfolio_value

    ):

    print(

        "\nBuilding portfolio actions...\n"
    )

    position_lookup = (

        position_df.set_index(
            "symbol"
        )
    )

    risk_lookup = (

        portfolio_risk_df.set_index(
            "symbol"
        )
    )

    rows = []

    for _, row in rebalance_df.iterrows():

        symbol = row["symbol"]

        difference = abs(

            row[
                "difference"
            ]
        )

        portfolio_risk = (

            risk_lookup.loc[
                symbol,
                "portfolio_risk"
            ]

            if symbol in risk_lookup.index

            else 0
        )

        value = 0

        if symbol in position_lookup.index:

            value = round(

                position_lookup.loc[
                    symbol,
                    "executable_position_value"
                ],

                2
            )

        rebalance_action = (

            row["action"]
        )

        if rebalance_action == "REDUCE":

            action = "REDUCE"

            if difference > 30:

                reason = (

                    "Severely overweight position"
                )

            elif difference > 10:

                reason = (

                    "Moderately overweight position"
                )

            else:

                reason = (

                    "Slightly overweight position"
                )

        elif value > 0:

            action = "BUY"

            reason = (

                "Meaningful allocation opportunity"
            )

        else:

            action = "HOLD"

            reason = (

                "Near target allocation"
            )

        if action == "REDUCE":

            if difference > 30:

                priority = "HIGH"

            elif difference > 10:

                priority = "MEDIUM"

            else:

                priority = "LOW"

        elif action == "BUY":

            if value > 2000:

                priority = "HIGH"

            elif value > 500:

                priority = "MEDIUM"

            else:

                priority = "LOW"

        else:

            priority = "LOW"

        if (

            action == "HOLD"

            and value <= 0

            and portfolio_risk <= 0

        ):

            continue

        trade_value = 0

        if action == "REDUCE":

            trade_value = round(

                portfolio_value

                * (

                    difference / 100
                ),

                2
            )

        elif action == "BUY":

            trade_value = value

        rows.append({

            "symbol":
                symbol,

            "action":
                action,

            "priority":
                priority,

            "trade_value":
                trade_value,

            "reason":
                reason
        })

    result_df = pd.DataFrame(
        rows
    )

    return result_df.sort_values(

        by="priority",

        ascending=True
    )

