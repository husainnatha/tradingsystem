import pandas as pd

from src.services.capital_service import (
    CapitalService
)

from app.engine.portfolio_summary import (
    get_portfolio_summary
)

def build_capital_summary():

    state = (
        build_capital_state()
    )

    rows = []

    for key, value in state.items():

        rows.append({

            "Metric":
                key,

            "Value":
                value
        })

    return pd.DataFrame(
        rows
    )

def build_capital_state():

    config = (
        CapitalService
        .get_capital_config()
    )

    cash = (
        config[
            "cash"
        ]
    )

    target_cash_reserve = (
        config[
            "target_cash_reserve"
        ]
    )

    max_deployment_percent = (
        config[
            "max_deployment_percent"
        ]
    )

    summary = (
        get_portfolio_summary()
    )

    invested_value = (
        summary[
            "total_portfolio_value"
        ]
    )

    portfolio_value = (

        invested_value

        + cash
    )

    cash_shortfall = max(

        0,

        target_cash_reserve

        - cash
    )

    cash_surplus = max(

        0,

        cash

        - target_cash_reserve
    )

    cash_percentage = round(

        (
            cash
            /
            portfolio_value
        ) * 100,

        2

    ) if portfolio_value != 0 else 0

    invested_percentage = round(

        (
            invested_value
            /
            portfolio_value
        ) * 100,

        2

    ) if portfolio_value != 0 else 0

    cash_funding_ratio = round(

        cash
        /
        target_cash_reserve,

        2

    ) if target_cash_reserve != 0 else 0

    target_invested_value = round(

        portfolio_value

        * (

            max_deployment_percent
            / 100
        ),

        2
    )

    deployment_difference = round(

        invested_value

        - target_invested_value,

        2
    )

    required_sale_value = max(

        0,

        deployment_difference
    )

    available_cash = max(

        0,

        cash

        - target_cash_reserve
    )

    deployable_capital = min(

        available_cash,

        max(
            0,
            -deployment_difference
        )
    )

    required_sale_for_cash = (
        cash_shortfall
    )

    required_sale_for_deployment = max(

        0,

        deployment_difference
    )

    cash_target_achievable = (

        required_sale_for_cash

        <=

        portfolio_value
    )

    if cash_funding_ratio < 0.5:

        capital_status = (
            "CRITICAL"
        )

    elif cash_funding_ratio < 1:

        capital_status = (
            "UNDERFUNDED"
        )

    elif deployment_difference > 0:

        capital_status = (
            "OVERDEPLOYED"
        )

    else:

        capital_status = (
            "HEALTHY"
        )
        
    summary = get_portfolio_summary()

    print("\nPORTFOLIO SUMMARY")
    print(summary)
    print()

    print(
        "\nTOTAL PORTFOLIO VALUE:",
        summary["total_portfolio_value"]
    )

    return {

        "cash":
            cash,

        "target_cash_reserve":
            target_cash_reserve,

        "cash_shortfall":
            cash_shortfall,

        "cash_surplus":
            cash_surplus,

        "portfolio_value":
            portfolio_value,

        "invested_value":
            invested_value,

        "cash_percentage":
            cash_percentage,

        "invested_percentage":
            invested_percentage,

        "cash_funding_ratio":
            cash_funding_ratio,

        "max_deployment_percent":
            max_deployment_percent,

        "target_invested_value":
            target_invested_value,

        "deployment_difference":
            deployment_difference,

        "required_sale_value":
            required_sale_value,

        "available_cash":
            available_cash,

        "deployable_capital":
            deployable_capital,

        "required_sale_for_cash":
            required_sale_for_cash,

        "required_sale_for_deployment":
            required_sale_for_deployment,

        "cash_target_achievable":
            cash_target_achievable,

        "capital_status":
            capital_status
    }

if __name__ == "__main__":

    state = build_capital_state()

    print()

    for key, value in state.items():

        print(f"{key}: {value}")

    print()

    

