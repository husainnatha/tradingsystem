from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)

df = (

    build_portfolio_risk()
)

print(

    "\nPORTFOLIO RISK:\n"
)

print(

    df.to_string()
)