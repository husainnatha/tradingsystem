from app.engine.capital_engine import build_capital_state
from app.engine.macro_regime_engine import build_macro_regime


def build_contextual_decisions(opportunity_df):

    decisions = []

    # --- Capital State ---
    capital_state = build_capital_state()
    capital_status = capital_state["capital_status"]
    required_sale_value = capital_state["required_sale_value"]
    cash_shortfall = capital_state["cash_shortfall"]

    # --- Macro Regime ---
    macro_regime = build_macro_regime()
    regime = macro_regime["regime"]

    # -------------------------
    # DECISION LOGIC
    # -------------------------

    # 1. CRITICAL CAPITAL → Raise cash immediately
    if capital_status == "CRITICAL":

        decisions.append({
            "priority": 1,
            "decision": "RAISE_CASH",
            "reason": "Cash reserve below target"
        })

    if required_sale_value > 0:
        decisions.append({
            "priority": 2,
            "decision": "TRIM_POSITIONS",
            "reason": f"Portfolio overdeployed by £{required_sale_value:,.2f}"
        })

    if regime == "RISK_OFF":
        decisions.append({
            "priority": 3,
            "decision": "DEFENSIVE_ONLY",
            "reason": "Macro regime is risk off"
        })

    # 2. HEALTHY + NO SHORTFALL + RISK ON → Buy top opportunity
    if (
        capital_status == "HEALTHY"
        and cash_shortfall == 0
        and regime == "RISK_ON"
        and not opportunity_df.empty
    ):
        top_stock = opportunity_df.iloc[0]["symbol"]

        decisions.append({
            "priority": 4,
            "decision": f"BUY_{top_stock}",
            "reason": "Highest opportunity score"
        })

    #3 NO DECISION INSTANCE
    if len(decisions) == 0:

        decisions.append({

            "priority": 99,

            "decision": "HOLD",

            "reason":
                 f"No higher priority action identified. Macro regime = {regime}"
        })

    # Sort by priority
    decisions = sorted(decisions, key=lambda x: x["priority"])

    return decisions
