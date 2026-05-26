from app.engine.risk_engine import (

    build_risk_engine
)

risk_df = (

    build_risk_engine()
)

risk_df = (

    risk_df.sort_values(

        by="risk_score",

        ascending=False
    )
)

print(

    "\nRISK INTELLIGENCE:\n"
)

print(

    risk_df.to_string()
)