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

    "\nPOSITION SIZING:\n"
)

for _, row in df.iterrows():

    print(

        f"{row['symbol']} | "

        f"{row['rating']} | "

        f"Risk={row['risk_score']} | "

        f"PortfolioRisk={row['portfolio_risk']:.4f} | "

        f"Macro={row['macro_regime']} | "

        f"Allocation={row['suggested_allocation_pct']}% | "

        f"Value=£{row['suggested_position_value']} | "

        f"Shares={row['suggested_shares']}"
    )

    print(

        f"Why: {row['explanation']}\n"
    )