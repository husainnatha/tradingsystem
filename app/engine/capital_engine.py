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

        {

            "Metric":
                "PortfolioValue",

            "Value":
                portfolio_value
        },

        {

            "Metric":
                "CurrentCash",

            "Value":
                current_cash
        },

        {

            "Metric":
                "EmergencyReserve",

            "Value":
                emergency_reserve
        },

        {

            "Metric":
                "TargetCashReserve",

            "Value":
                target_cash_reserve
        },

        {

            "Metric":
                "MonthlyContributions",

            "Value":
                monthly_contributions
        },

        {

            "Metric":
                "MaxDeploymentPercent",

            "Value":
                max_deployment_percent
        },

        {

            "Metric":
                "DeployableCapital",

            "Value":
                deployable_capital
        },

        {

            "Metric":
                "AvailableToInvest",

            "Value":
                available_to_invest
        }
    ]

    return pd.DataFrame(
        rows
    )