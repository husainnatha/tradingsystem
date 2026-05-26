from app.engine.decision_engine import (
    build_decisions
)

from app.engine.action_engine import (
    build_actions
)

from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)

from app.reports.tax_dashboard import (
    build_tax_dashboard
)

actions = build_actions(...)
risk = build_portfolio_risk()
tax = build_tax_dashboard()

df = build_decisions(

    action_df=actions,

    risk_df=risk,

    tax_df=tax
)

print(df)