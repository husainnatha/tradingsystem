# -----------------------------------
# SECTOR MAP
# -----------------------------------

SECTOR_MAP = {

    "NVDA": "AI_SEMICONDUCTORS",

    "AMD": "AI_SEMICONDUCTORS",

    "NOW": "AI_SOFTWARE",

    "META": "DIGITAL_ADVERTISING",

    "AMZN": "CLOUD_ECOMMERCE",

    "TSLA": "EV_AUTONOMY",

    "POET": "OPTICAL_NETWORKING",

    "LWLG": "OPTICAL_NETWORKING",

    "HOOD": "FINTECH",

    "CRWV": "AI_INFRASTRUCTURE"
}

# -----------------------------------
# GET SECTOR
# -----------------------------------

def get_sector(

    symbol
):

    return SECTOR_MAP.get(

        symbol,

        "UNKNOWN"
    )