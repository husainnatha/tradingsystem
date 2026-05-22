# -----------------------------------
# MOCK MARKET PRICES
# -----------------------------------

MARKET_PRICES = {

    "META": 740,
    "HOOD": 65,
    "AMD": 180,
    "CRWV": 95,
    "LWLG": 7,
    "POET": 12,
    "NVDA": 1400,
    "TSLA": 260,
    "AMZN": 210,
    "GOOG": 190,
    "PLTR": 70,
    "TEST": 30
}


# -----------------------------------
# GET MARKET PRICE
# -----------------------------------

def get_market_price(symbol):

    if symbol not in MARKET_PRICES:

        return None

    return MARKET_PRICES[symbol]