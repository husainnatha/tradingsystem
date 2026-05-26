import pandas as pd

from app.engine.action_engine import (
    build_actions
)

from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)

from app.reports.tax_dashboard import (
    build_tax_dashboard
)

def build_decisions(

    action_df,

    risk_df,

    tax_df
):

    rows = []

    for _, row in action_df.iterrows():

        decision = row["action"]

        reason = row["reason"]

        rows.append({

            "symbol":
                row["symbol"],

            "decision":
                decision,

            "priority":
                row["priority"],

            "reason":
                reason
        })

    return pd.DataFrame(
        rows
    )