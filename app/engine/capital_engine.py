import pandas as pd

from src.services.capital_service import (
    CapitalService
)


def build_capital_summary():

    config = (
        CapitalService
        .get_capital_config()
    )

    emergency_reserve = (
        config[
            "emergency_reserve"
        ]
    )

    target_cash_reserve = (
        config[
            "target_cash_reserve"
        ]
    )

    monthly_contributions = (
        config[
            "monthly_contributions"
        ]
    )

    max_deployment_percent = (
        config[
            "max_deployment_percent"
        ]
    )

    portfolio_value = 40000

    current_cash = 15000

    deployable_capital = (

        portfolio_value

        * (

            max_deployment_percent
            / 100
        )
    )

    available_to_invest = (

        deployable_capital

        - current_cash
    )

    rows = [

    # -----------------------------------
    # RUNTIME
    # -----------------------------------

    {

        "Section":
            "RUNTIME",

        "Metric":
            "Environment",

        "Value":
            "DEV"
    },

    {

        "Section":
            "RUNTIME",

        "Metric":
            "MarketRegime",

        "Value":
            "RISK_ON"
    },

    # -----------------------------------
    # CAPITAL
    # -----------------------------------

    {

        "Section":
            "CAPITAL",

        "Metric":
            "PortfolioValue",

        "Value":
            portfolio_value
    },

    {

        "Section":
            "CAPITAL",

        "Metric":
            "CurrentCash",

        "Value":
            current_cash
    },

    {

        "Section":
            "CAPITAL",

        "Metric":
            "EmergencyReserve",

        "Value":
            emergency_reserve
    },

    {

        "Section":
            "CAPITAL",

        "Metric":
            "TargetCashReserve",

        "Value":
            target_cash_reserve
    },

    {

        "Section":
            "CAPITAL",

        "Metric":
            "DeployableCapital",

        "Value":
            deployable_capital
    },

    {

        "Section":
            "CAPITAL",

        "Metric":
            "AvailableToInvest",

        "Value":
            available_to_invest
    },

    # -----------------------------------
    # RISK
    # -----------------------------------

    {

        "Section":
            "RISK",

        "Metric":
            "CashRatio",

        "Value":
            round(

                current_cash

                / portfolio_value,

                4
            )
    },

    {

        "Section":
            "RISK",

        "Metric":
            "DeploymentPct",

        "Value":
            round(

                deployable_capital

                / portfolio_value,

                4
            )
    }
]

    return pd.DataFrame(
        rows
    )