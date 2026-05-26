from app.engine.position_sizing_engine import (
    build_position_sizing
)

from app.config.watchlist import (
    WATCHLIST
)

df = build_position_sizing(

    watchlist=WATCHLIST,

    portfolio_value=100000
)

print(

    f"{row['symbol']} | "

    f"{row['rating']} | "

    f"Risk={row['risk_score']} | "

    f"Macro={row['macro_regime']} | "

    f"Multiplier={row['macro_multiplier']} | "

    f"Allocation={row['suggested_allocation_pct']}%"
)