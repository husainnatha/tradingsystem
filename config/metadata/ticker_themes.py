THEMES = [

    "AI",

    "PHOTONICS",

    "SEMICONDUCTORS",

    "NETWORKING",

    "DATA_CENTRES",

    "CYBERSECURITY",

    "QUANTUM",

    "AUTONOMY",

    "ROBOTICS",

    "HEALTHCARE",

    "ENERGY",

    "FINTECH",

    "CLOUD",

    "AUTOMATION",

    "CONSUMER",

    "DEFENSIVE",

    "STREAMING",

    "ENTERTAINMENT",

    "SMALL_CAPS",

    "INNOVATION",

    "MARKET"
]

def get_ticker_themes(

    symbol
):

    return THEMES.get(

        symbol,

        "UNKNOWN"
    )