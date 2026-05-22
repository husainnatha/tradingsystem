import pandas as pd

from datetime import date

from app.engine.inventory_engine import (
    build_inventory_state
)

from app.config.strategy_profiles import (
    get_strategy_profile
)

from app.services.technical_indicator_service import (
    get_technical_indicators
)

# -----------------------------------
# NORMALISE SCORE
# -----------------------------------

def normalise_series(series):

    min_val = series.min()

    max_val = series.max()

    # -----------------------------------
    # PREVENT DIVIDE BY ZERO
    # -----------------------------------

    if min_val == max_val:

        return pd.Series(

            [1.0] * len(series),

            index=series.index
        )

    return (

        (
            series - min_val
        )

        /

        (
            max_val - min_val
        )
    )
# -----------------------------------
# BUILD RANKING ENGINE
# -----------------------------------

def build_ranked_inventory(

    strategy="tax_saver"
):

    inventory_df = build_inventory_state()

    profile = get_strategy_profile(
        strategy
    )

    # -----------------------------------
    # FILTER ACTIVE INVENTORY
    # -----------------------------------

    inventory_df = inventory_df[

        inventory_df[
            "remaining_quantity"
        ] > 0
    ].copy()

        # -----------------------------------
    # LOAD TECHNICAL INDICATORS
    # -----------------------------------

    inventory_df[
        "technical_data"
    ] = inventory_df[
        "symbol"
    ].apply(
        get_technical_indicators
    )

    inventory_df[
        "bullish_trend"
    ] = inventory_df[
        "technical_data"
    ].apply(

        lambda x:

        x.get(
            "bullish_trend",
            False
        )

        if x else False
    )

    inventory_df[
        "rsi"
    ] = inventory_df[
        "technical_data"
    ].apply(

        lambda x:

        x.get(
            "rsi",
            50
        )

        if x else 50
    )

    # -----------------------------------
    # HOLDING PERIOD
    # -----------------------------------

    today = pd.Timestamp.today()

    inventory_df[
        "holding_days"
    ] = (

        today

        -

        pd.to_datetime(

            inventory_df[
                "trade_date"
            ]
        )

    ).dt.days

    # -----------------------------------
    # TAX EFFICIENCY SCORE
    # LOWER GAIN = BETTER SELL
    # -----------------------------------

    inventory_df[
        "gain_per_share"
    ] = (

        inventory_df[
            "unrealised_gain_gbp"
        ]

        /

        inventory_df[
            "remaining_quantity"
        ]
    )

    inventory_df[
        "tax_efficiency_score"
    ] = 1 - normalise_series(

        inventory_df[
            "gain_per_share"
        ]
    )

    # -----------------------------------
    # POSITION SIZE SCORE
    # BIGGER POSITION = HIGHER RISK
    # -----------------------------------

    inventory_df[
        "position_value"
    ] = inventory_df[
        "market_value_gbp"
    ]

    inventory_df[
        "position_risk_score"
    ] = normalise_series(

        inventory_df[
            "position_value"
        ]
    )

    # -----------------------------------
    # HOLDING PERIOD SCORE
    # OLDER POSITIONS SCORE HIGHER
    # -----------------------------------

    inventory_df[
        "holding_period_score"
    ] = normalise_series(

        inventory_df[
            "holding_days"
        ]
    )

        # -----------------------------------
    # MOMENTUM SCORE
    # -----------------------------------

    inventory_df[
        "momentum_score"
    ] = 0

    inventory_df.loc[

        inventory_df[
            "bullish_trend"
        ] == True,

        "momentum_score"

    ] = 1

    # -----------------------------------
    # RSI PENALTY
    # OVERBOUGHT = LESS ATTRACTIVE SELL
    # -----------------------------------

    inventory_df[
        "rsi_score"
    ] = 1 - (

        inventory_df[
            "rsi"
        ] / 100
    )

    # -----------------------------------
    # TOTAL AI SCORE
    # -----------------------------------

    inventory_df[
        "ai_score"
    ] = round(

        (

            inventory_df[
                "tax_efficiency_score"
            ]

            *

            profile[
                "tax_efficiency_weight"
            ]

            +

            inventory_df[
                "position_risk_score"
            ]

            *

            profile[
                "position_risk_weight"
            ]

            +

            inventory_df[
                "holding_period_score"
            ]

            *

            profile[
                "holding_period_weight"
            ]

            +

            inventory_df[
                "momentum_score"
            ] * 0.2

            +

            inventory_df[
                "rsi_score"
            ] * 0.1
        ),

        4
    )

    # -----------------------------------
    # SORT BEST SELL CANDIDATES
    # -----------------------------------

    inventory_df = inventory_df.sort_values(

        by="ai_score",

        ascending=False
    )

    return inventory_df