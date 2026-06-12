import pandas as pd

from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)

from app.engine.position_sizing_engine import (
    build_position_sizing
)

from app.engine.risk_intelligence_engine import (
    build_risk_engine
)


# -----------------------------------
# BUILD REBALANCING ENGINE
# -----------------------------------

def build_rebalancing(
    market_context,
    portfolio_value
):

    # -----------------------------------
    # CURRENT PORTFOLIO
    # -----------------------------------

    current_df = (

        build_portfolio_risk(
            market_context
        )
    )

    current_lookup = (

        current_df.set_index(
            "symbol"
        )
    )

    # -----------------------------------
    # TARGET ALLOCATIONS
    # -----------------------------------

    risk_intelligence_df = (

    build_risk_engine(

            symbols=list(

                market_context
                .get_all()
                .keys()
            ),

            verbose=False
        )
    )

    target_df = (

        build_position_sizing(

            market_context=market_context,

            portfolio_value=portfolio_value,

            risk_intelligence_df=risk_intelligence_df
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