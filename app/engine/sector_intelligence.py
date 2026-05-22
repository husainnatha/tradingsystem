import pandas as pd

from app.engine.inventory_engine import (
    build_inventory_state
)

from app.config.sector_map import (
    get_sector
)

# -----------------------------------
# BUILD SECTOR EXPOSURE
# -----------------------------------

def build_sector_exposure():

    inventory_df = build_inventory_state()

    # -----------------------------------
    # ACTIVE POSITIONS ONLY
    # -----------------------------------

    inventory_df = inventory_df[

        inventory_df[
            "remaining_quantity"
        ] > 0
    ].copy()

    # -----------------------------------
    # ADD SECTORS
    # -----------------------------------

    inventory_df[
        "sector"
    ] = inventory_df[
        "symbol"
    ].apply(
        get_sector
    )

    # -----------------------------------
    # CALCULATE TOTAL PORTFOLIO VALUE
    # -----------------------------------

    total_value = inventory_df[
        "market_value_gbp"
    ].sum()

    # -----------------------------------
    # GROUP BY SECTOR
    # -----------------------------------

    sector_df = (

        inventory_df.groupby(
            "sector"
        )[

            "market_value_gbp"

        ]

        .sum()

        .reset_index()
    )

    # -----------------------------------
    # EXPOSURE %
    # -----------------------------------

    sector_df[
        "exposure_pct"
    ] = round(

        (

            sector_df[
                "market_value_gbp"
            ]

            /

            total_value
        )

        * 100,

        2
    )

    # -----------------------------------
    # CONCENTRATION RISK
    # -----------------------------------

    sector_df[
        "concentration_risk"
    ] = sector_df[
        "exposure_pct"
    ].apply(

        lambda x:

        "HIGH"

        if x >= 35

        else (

            "MEDIUM"

            if x >= 20

            else "LOW"
        )
    )

    # -----------------------------------
    # SORT LARGEST FIRST
    # -----------------------------------

    sector_df = sector_df.sort_values(

        by="exposure_pct",

        ascending=False
    )

    return sector_df