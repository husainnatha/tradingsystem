import pandas as pd

from app.engine.rebalancing_engine import (
    build_rebalancing
)

from app.engine.position_sizing_engine import (
    build_position_sizing
)

from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)

from app.config.watchlist import (
    WATCHLIST
)

# -----------------------------------
# BUILD ACTION ENGINE
# -----------------------------------

def build_actions(

    portfolio_value=100000
):

    print(

        "\nBuilding portfolio actions...\n"
    )

    # -----------------------------------
    # LOAD DATA
    # -----------------------------------

    rebalance_df = (

        build_rebalancing(
            portfolio_value
        )
    )

    position_df = (

        build_position_sizing(

            watchlist=WATCHLIST,

            portfolio_value=portfolio_value
        )
    )

    risk_df = (

        build_portfolio_risk()
    )

    # -----------------------------------
    # LOOKUPS
    # -----------------------------------

    position_lookup = (

        position_df.set_index(
            "symbol"
        )
    )

    risk_lookup = (

        risk_df.set_index(
            "symbol"
        )
    )

    rows = []

    # -----------------------------------
    # ACTIONS
    # -----------------------------------

    for _, row in rebalance_df.iterrows():

        symbol = row["symbol"]

        portfolio_risk = (

            risk_lookup.loc[
                symbol,
                "portfolio_risk"
            ]

            if symbol in risk_lookup.index

            else 0
        )

        # -----------------------------------
        # POSITION VALUE
        # -----------------------------------

        value = 0

        if symbol in position_lookup.index:

            value = round(

                position_lookup.loc[
                    symbol,
                    "suggested_position_value"
                ],

                2
            )

        # -----------------------------------
        # DECISION RULES
        # -----------------------------------

        rebalance_action = row["action"]

        reason = ""

        # High risk → reduce

        if portfolio_risk > 0.25:

            action = "REDUCE"

            reason = (
                "High portfolio concentration and risk"
            )

        # Meaningful opportunity

        elif value >= 1000:

            action = "BUY"

            reason = (
                "Meaningful allocation opportunity"
            )

        # Small adjustment only

        else:

            action = "HOLD"

            reason = (
                "Near target allocation"
            )

        # -----------------------------------
        # PRIORITY RULES
        # -----------------------------------

        if action == "REDUCE":

            priority = "HIGH"

        elif action == "BUY":

            if portfolio_risk > 0.10:

                priority = "MEDIUM"

            else:

                priority = "LOW"

        else:

            priority = "LOW"

        # -----------------------------------
        # SKIP EMPTY
        # -----------------------------------

        if action == "HOLD" and value == 0:

            continue

        rows.append({

            "symbol":
                symbol,

            "action":
                action,

            "priority":
                priority,

            "value":
                value,

            "reason":
                reason
        })

    # -----------------------------------
    # RETURN RESULTS
    # -----------------------------------

    result_df = pd.DataFrame(

        rows
    )

    return result_df.sort_values(

        by="priority",

        ascending=True
    )