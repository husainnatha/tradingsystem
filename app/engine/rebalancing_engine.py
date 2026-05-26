import pandas as pd

from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)

from app.engine.position_sizing_engine import (
    build_position_sizing
)

from app.config.watchlist import (
    WATCHLIST
)

# -----------------------------------
# BUILD REBALANCING ENGINE
# -----------------------------------

def build_rebalancing(

    portfolio_value=100000
):

    # -----------------------------------
    # CURRENT PORTFOLIO
    # -----------------------------------

    current_df = (

        build_portfolio_risk()
    )

    current_lookup = (

        current_df.set_index(
            "symbol"
        )
    )

    # -----------------------------------
    # TARGET ALLOCATIONS
    # -----------------------------------

    target_df = (

        build_position_sizing(

            watchlist=WATCHLIST,

            portfolio_value=portfolio_value
        )
    )

    target_lookup = (

        target_df.set_index(
            "symbol"
        )
    )

    rows = []

    # -----------------------------------
    # COMPARE CURRENT VS TARGET
    # -----------------------------------

    for symbol in current_lookup.index:

        current_weight = round(

            current_lookup.loc[
                symbol,
                "concentration"
            ] * 100,

            2
        )

        target_weight = (

            target_lookup.loc[
                symbol,
                "suggested_allocation_pct"
            ]

            if symbol in target_lookup.index

            else 0
        )

        difference = round(

            current_weight
            - target_weight,

            2
        )

        # -----------------------------------
        # ACTIONS
        # -----------------------------------

        if difference > 5:

            action = "REDUCE"

            reason = (

                "Overweight exposure"
            )

        elif difference < -5:

            action = "ACCUMULATE"

            reason = (

                "Underweight exposure"
            )

        else:

            action = "HOLD"

            reason = (

                "Near target allocation"
            )

        rows.append({

            "symbol":
                symbol,

            "current_weight":
                current_weight,

            "target_weight":
                target_weight,

            "difference":
                difference,

            "action":
                action,

            "reason":
                reason
        })

    return pd.DataFrame(

        rows

    ).sort_values(

        by="difference",

        ascending=False
    )