from app.services.macro_service import (
    get_macro_data
)

# -----------------------------------
# BUILD MACRO REGIME
# -----------------------------------

def build_macro_regime():

    macro = get_macro_data()

    score = 0

    reasons = []

    # -----------------------------------
    # VIX
    # -----------------------------------

    vix = macro.get(

        "VIX",

        {}
    ).get(

        "price",

        20
    )

    if vix > 25:

        score -= 2

        reasons.append(

            "high market fear"
        )

    elif vix < 18:

        score += 1

        reasons.append(

            "low volatility"
        )

    # -----------------------------------
    # US10Y
    # -----------------------------------

    us10 = macro.get(

        "US10Y",

        {}
    ).get(

        "daily_change_pct",

        0
    )

    if us10 > 1:

        score -= 1

        reasons.append(

            "rising yields"
        )

    elif us10 < -1:

        score += 1

        reasons.append(

            "falling yields"
        )

    # -----------------------------------
    # QQQ
    # -----------------------------------

    qqq_trend = macro.get(

        "QQQ",

        {}
    ).get(

        "trend",

        False
    )

    if qqq_trend:

        score += 2

        reasons.append(

            "growth trend positive"
        )

    else:

        score -= 2

        reasons.append(

            "growth trend weak"
        )

    # -----------------------------------
    # BTC
    # -----------------------------------

    btc = macro.get(

        "BTC",

        {}
    ).get(

        "daily_change_pct",

        0
    )

    if btc > 2:

        score += 1

        reasons.append(

            "risk appetite"
        )

    elif btc < -2:

        score -= 1

        reasons.append(

            "risk reduction"
        )

    # -----------------------------------
    # DETERMINE REGIME
    # -----------------------------------

    if score >= 1:

        regime = "RISK_ON"

    elif score <= -1:

        regime = "RISK_OFF"

    else:

        regime = "NEUTRAL"

    return {

        "regime": regime,

        "score": score,

        "reasons": reasons
    }