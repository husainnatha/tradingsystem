# -----------------------------------
# REGIME SECTOR PREFERENCES
# -----------------------------------

MACRO_SECTOR_PREFERENCES = {

    "RISK_ON": {

        "AI_SEMICONDUCTORS": 1.0,
        "AI_SOFTWARE": 0.9,
        "AI_INFRASTRUCTURE": 0.9,
        "OPTICAL_NETWORKING": 0.8,
        "EV_AUTONOMY": 0.7,
        "FINTECH": 0.7
    },

    "NEUTRAL": {

        "AI_SEMICONDUCTORS": 0.7,
        "AI_SOFTWARE": 0.7,
        "AI_INFRASTRUCTURE": 0.7,
        "OPTICAL_NETWORKING": 0.7,
        "EV_AUTONOMY": 0.7,
        "FINTECH": 0.7
    },

    "RISK_OFF": {

        "AI_SEMICONDUCTORS": 0.3,
        "AI_SOFTWARE": 0.4,
        "AI_INFRASTRUCTURE": 0.4,
        "OPTICAL_NETWORKING": 0.2,
        "EV_AUTONOMY": 0.2,
        "FINTECH": 0.3
    }
}

# -----------------------------------
# LOOKUP
# -----------------------------------

def get_sector_bias(

    regime,

    sector
):

    return (

        MACRO_SECTOR_PREFERENCES

        .get(
            regime,
            {}
        )

        .get(
            sector,
            0.5
        )
    )