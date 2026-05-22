# -----------------------------------
# STRATEGY PROFILES
# -----------------------------------

STRATEGY_PROFILES = {

    "tax_saver": {

        "tax_efficiency_weight": 0.6,

        "position_risk_weight": 0.2,

        "holding_period_weight": 0.2
    },

    "growth": {

        "tax_efficiency_weight": 0.2,

        "position_risk_weight": 0.2,

        "holding_period_weight": 0.6
    },

    "risk_reduction": {

        "tax_efficiency_weight": 0.2,

        "position_risk_weight": 0.6,

        "holding_period_weight": 0.2
    }
}

# -----------------------------------
# GET STRATEGY PROFILE
# -----------------------------------

def get_strategy_profile(

    strategy
):

    if strategy not in STRATEGY_PROFILES:

        raise Exception(

            f"Unknown strategy: "
            f"{strategy}"
        )

    return STRATEGY_PROFILES[
        strategy
    ]